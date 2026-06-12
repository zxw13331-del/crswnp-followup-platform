import json
import random
from datetime import date, timedelta
from pathlib import Path

from sqlalchemy.orm import Session

from .models import FollowupPlan, FollowupRecord, Patient, RiskAssessment, User
from .risk import calculate_risk

SCHEDULE_PATH = Path(__file__).parent / "config" / "followup_schedule.json"


def add_months(base: date, months: int) -> date:
    return base + timedelta(days=months * 30)


def seed_demo_data(db: Session) -> None:
    if db.query(Patient).count() >= 60:
        return

    db.query(FollowupRecord).delete()
    db.query(FollowupPlan).delete()
    db.query(RiskAssessment).delete()
    db.query(Patient).delete()
    db.query(User).delete()
    db.add(User(username="demo", display_name="科研演示用户", role="researcher"))

    rng = random.Random(20260612)
    schedule = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))["nodes"]
    today = date.today()
    treatment_options = ["鼻喷雾", "大容量鼻腔冲洗", "鼻喷雾 + 大容量鼻腔冲洗"]
    outcomes = ["症状改善", "症状稳定", "疑似复发", "需加强随访"]

    for i in range(1, 73):
        group = i % 3
        if group == 0:
            age = rng.randint(24, 52)
            eos = round(rng.uniform(1.0, 4.5), 1)
            tissue = rng.choice([0, 1])
            snot = rng.randint(8, 34)
            polyp = rng.randint(0, 3)
            adherence = round(rng.uniform(0.72, 0.98), 2)
            asthma = rng.random() < 0.12
            prior = rng.choice([0, 0, 1])
        elif group == 1:
            age = rng.randint(32, 68)
            eos = round(rng.uniform(4.0, 8.5), 1)
            tissue = rng.choice([1, 2])
            snot = rng.randint(28, 64)
            polyp = rng.randint(3, 6)
            adherence = round(rng.uniform(0.45, 0.78), 2)
            asthma = rng.random() < 0.35
            prior = rng.choice([0, 1, 1, 2])
        else:
            age = rng.randint(38, 78)
            eos = round(rng.uniform(8.0, 16.0), 1)
            tissue = rng.choice([2, 3])
            snot = rng.randint(55, 98)
            polyp = rng.randint(5, 8)
            adherence = round(rng.uniform(0.12, 0.55), 2)
            asthma = rng.random() < 0.68
            prior = rng.choice([1, 2, 2, 3])

        patient = Patient(
            demo_code=f"CRS-DEMO-{i:03d}",
            sex=rng.choice(["男", "女"]),
            age=age,
            surgery_date=today - timedelta(days=rng.randint(25, 430)),
            asthma=asthma,
            allergic_rhinitis=rng.random() < (0.55 if group else 0.25),
            prior_surgery_count=prior,
            eosinophil_percent=eos,
            tissue_eosinophil_level=tissue,
            snot22_score=snot,
            polyp_score=polyp,
            adherence_score=adherence,
            treatment_plan=treatment_options[i % len(treatment_options)],
        )
        db.add(patient)
        db.flush()

        risk = calculate_risk(patient)
        db.add(RiskAssessment(patient_id=patient.id, **risk))

        for node in schedule:
            scheduled = add_months(patient.surgery_date, node["month"])
            if scheduled < today - timedelta(days=14):
                status = "completed" if rng.random() < 0.75 else "overdue"
            elif scheduled < today:
                status = "overdue" if rng.random() < 0.65 else "completed"
            else:
                status = "pending"
            plan = FollowupPlan(
                patient_id=patient.id,
                title=node["title"],
                scheduled_date=scheduled,
                status=status,
                checklist="、".join(node["items"]),
            )
            db.add(plan)
            db.flush()
            if status == "completed":
                symptom_score = max(0, int(patient.snot22_score * rng.uniform(0.35, 0.85)))
                if risk["risk_level"] == "high" and rng.random() < 0.35:
                    outcome = "疑似复发"
                else:
                    outcome = rng.choice(outcomes[:3])
                db.add(FollowupRecord(
                    plan_id=plan.id,
                    visit_date=scheduled + timedelta(days=rng.randint(-5, 7)),
                    symptom_score=symptom_score,
                    outcome=outcome,
                    notes="模拟随访记录：用于科研概念验证。",
                ))
    db.commit()
