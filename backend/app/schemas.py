from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class PatientBase(BaseModel):
    sex: str = "女"
    age: int = Field(ge=18, le=85)
    surgery_date: date
    asthma: bool = False
    allergic_rhinitis: bool = False
    prior_surgery_count: int = Field(ge=0, le=5)
    eosinophil_percent: float = Field(ge=0, le=30)
    tissue_eosinophil_level: int = Field(ge=0, le=3)
    snot22_score: int = Field(ge=0, le=110)
    polyp_score: int = Field(ge=0, le=8)
    adherence_score: float = Field(ge=0, le=1)
    treatment_plan: str


class PatientCreate(PatientBase):
    demo_code: str | None = None


class PatientUpdate(PatientBase):
    pass


class RiskAssessmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model_version: str
    probability: float
    risk_level: str
    explanation: str
    disclaimer: str
    created_at: datetime


class FollowupRecordOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    visit_date: date
    symptom_score: int
    outcome: str
    notes: str


class FollowupPlanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    patient_id: int
    title: str
    scheduled_date: date
    status: str
    checklist: str
    records: list[FollowupRecordOut] = []


class PatientOut(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    demo_code: str
    created_at: datetime
    risk_assessments: list[RiskAssessmentOut] = []
    followup_plans: list[FollowupPlanOut] = []


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    display_name: str
    role: str


class DashboardOut(BaseModel):
    total_patients: int
    risk_counts: dict[str, int]
    followup_counts: dict[str, int]
    treatment_counts: dict[str, int]
    disclaimer: str


class StatsOut(BaseModel):
    risk_distribution: list[dict]
    followup_status_distribution: list[dict]
    outcome_distribution: list[dict]
    average_scores_by_risk: list[dict]
    disclaimer: str
