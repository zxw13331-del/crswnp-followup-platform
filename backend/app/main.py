import csv
import io
import json
from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from .database import Base, engine, get_db
from .models import FollowupPlan, FollowupRecord, Patient, RiskAssessment
from .risk import calculate_risk, load_risk_config
from .schemas import DashboardOut, LoginRequest, LoginResponse, PatientCreate, PatientOut, PatientUpdate, StatsOut
from .seed import seed_demo_data

app = FastAPI(title="CRSwNP 术后随访科研演示平台", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed_demo_data(db)
    finally:
        db.close()


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "科研演示 API 已启动"}


@app.post("/api/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    if payload.username == "demo" and payload.password == "demo123":
        return LoginResponse(token="demo-token", display_name="科研演示用户", role="researcher")
    raise HTTPException(status_code=401, detail="演示账号或密码错误")


def latest_risk_subquery(db: Session):
    return db.query(RiskAssessment.patient_id, func.max(RiskAssessment.id).label("risk_id")).group_by(RiskAssessment.patient_id).subquery()


@app.get("/api/dashboard", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db)):
    risk_sub = latest_risk_subquery(db)
    risk_rows = db.query(RiskAssessment.risk_level, func.count()).join(risk_sub, RiskAssessment.id == risk_sub.c.risk_id).group_by(RiskAssessment.risk_level).all()
    follow_rows = db.query(FollowupPlan.status, func.count()).group_by(FollowupPlan.status).all()
    treatment_rows = db.query(Patient.treatment_plan, func.count()).group_by(Patient.treatment_plan).all()
    return DashboardOut(
        total_patients=db.query(Patient).count(),
        risk_counts={k: v for k, v in risk_rows},
        followup_counts={k: v for k, v in follow_rows},
        treatment_counts={k: v for k, v in treatment_rows},
        disclaimer=load_risk_config()["disclaimer"],
    )


@app.get("/api/patients", response_model=list[PatientOut])
def list_patients(q: str = "", risk_level: str = "", db: Session = Depends(get_db)):
    query = db.query(Patient).options(joinedload(Patient.risk_assessments), joinedload(Patient.followup_plans).joinedload(FollowupPlan.records))
    if q:
        query = query.filter(Patient.demo_code.contains(q))
    patients = query.order_by(Patient.id).all()
    if risk_level:
        patients = [p for p in patients if p.risk_assessments and p.risk_assessments[-1].risk_level == risk_level]
    return patients


@app.post("/api/patients", response_model=PatientOut)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    count = db.query(Patient).count() + 1
    patient = Patient(**payload.model_dump(exclude={"demo_code"}), demo_code=payload.demo_code or f"CRS-DEMO-NEW-{count:03d}")
    db.add(patient)
    db.flush()
    db.add(RiskAssessment(patient_id=patient.id, **calculate_risk(patient)))
    db.commit()
    return get_patient(patient.id, db)


@app.get("/api/patients/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).options(joinedload(Patient.risk_assessments), joinedload(Patient.followup_plans).joinedload(FollowupPlan.records)).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="未找到模拟患者")
    return patient


@app.put("/api/patients/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="未找到模拟患者")
    for key, value in payload.model_dump().items():
        setattr(patient, key, value)
    db.add(RiskAssessment(patient_id=patient.id, **calculate_risk(patient)))
    db.commit()
    return get_patient(patient.id, db)


@app.post("/api/patients/{patient_id}/risk-assessment")
def recalculate_risk(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="未找到模拟患者")
    risk = RiskAssessment(patient_id=patient.id, **calculate_risk(patient))
    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk


@app.get("/api/followups")
def followups(status: str = Query(""), db: Session = Depends(get_db)):
    query = db.query(FollowupPlan, Patient.demo_code).join(Patient, Patient.id == FollowupPlan.patient_id).order_by(FollowupPlan.scheduled_date)
    if status:
        query = query.filter(FollowupPlan.status == status)
    return [
        {
            "id": plan.id,
            "patient_id": plan.patient_id,
            "demo_code": demo_code,
            "title": plan.title,
            "scheduled_date": plan.scheduled_date,
            "status": plan.status,
            "checklist": plan.checklist,
        }
        for plan, demo_code in query.all()
    ]


@app.get("/api/stats", response_model=StatsOut)
def stats(db: Session = Depends(get_db)):
    dash = dashboard(db)
    outcome_rows = db.query(FollowupRecord.outcome, func.count()).group_by(FollowupRecord.outcome).all()
    risk_sub = latest_risk_subquery(db)
    avg_rows = (
        db.query(RiskAssessment.risk_level, func.avg(Patient.snot22_score), func.avg(Patient.polyp_score))
        .join(risk_sub, RiskAssessment.id == risk_sub.c.risk_id)
        .join(Patient, Patient.id == RiskAssessment.patient_id)
        .group_by(RiskAssessment.risk_level)
        .all()
    )
    return StatsOut(
        risk_distribution=[{"name": k, "value": v} for k, v in dash.risk_counts.items()],
        followup_status_distribution=[{"name": k, "value": v} for k, v in dash.followup_counts.items()],
        outcome_distribution=[{"name": k, "value": v} for k, v in outcome_rows],
        average_scores_by_risk=[{"risk_level": k, "snot22": round(s or 0, 1), "polyp": round(p or 0, 1)} for k, s, p in avg_rows],
        disclaimer=load_risk_config()["disclaimer"],
    )


@app.get("/api/dictionary")
def dictionary():
    path = Path(__file__).parent / "config" / "data_dictionary.json"
    return json.loads(path.read_text(encoding="utf-8"))


@app.get("/api/export/patients.csv")
def export_patients(db: Session = Depends(get_db)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["demo_code", "sex", "age", "surgery_date", "risk_level", "risk_probability", "treatment_plan"])
    patients = db.query(Patient).options(joinedload(Patient.risk_assessments)).order_by(Patient.id).all()
    for p in patients:
        risk = p.risk_assessments[-1] if p.risk_assessments else None
        writer.writerow([p.demo_code, p.sex, p.age, p.surgery_date, risk.risk_level if risk else "", risk.probability if risk else "", p.treatment_plan])
    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=crswnp_demo_patients.csv"}
    return StreamingResponse(iter([output.getvalue()]), media_type="text/csv; charset=utf-8", headers=headers)
