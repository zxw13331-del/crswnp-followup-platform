from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(80))
    role: Mapped[str] = mapped_column(String(30), default="researcher")


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    demo_code: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    sex: Mapped[str] = mapped_column(String(10))
    age: Mapped[int] = mapped_column(Integer)
    surgery_date: Mapped[date] = mapped_column(Date)
    asthma: Mapped[bool] = mapped_column(Boolean, default=False)
    allergic_rhinitis: Mapped[bool] = mapped_column(Boolean, default=False)
    prior_surgery_count: Mapped[int] = mapped_column(Integer, default=0)
    eosinophil_percent: Mapped[float] = mapped_column(Float)
    tissue_eosinophil_level: Mapped[int] = mapped_column(Integer)
    snot22_score: Mapped[int] = mapped_column(Integer)
    polyp_score: Mapped[int] = mapped_column(Integer)
    adherence_score: Mapped[float] = mapped_column(Float)
    treatment_plan: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    risk_assessments: Mapped[list["RiskAssessment"]] = relationship(back_populates="patient", cascade="all, delete-orphan")
    followup_plans: Mapped[list["FollowupPlan"]] = relationship(back_populates="patient", cascade="all, delete-orphan")


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), index=True)
    model_version: Mapped[str] = mapped_column(String(50))
    probability: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(20))
    explanation: Mapped[str] = mapped_column(Text)
    disclaimer: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    patient: Mapped[Patient] = relationship(back_populates="risk_assessments")


class FollowupPlan(Base):
    __tablename__ = "followup_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), index=True)
    title: Mapped[str] = mapped_column(String(80))
    scheduled_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    checklist: Mapped[str] = mapped_column(Text)

    patient: Mapped[Patient] = relationship(back_populates="followup_plans")
    records: Mapped[list["FollowupRecord"]] = relationship(back_populates="plan", cascade="all, delete-orphan")


class FollowupRecord(Base):
    __tablename__ = "followup_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plan_id: Mapped[int] = mapped_column(ForeignKey("followup_plans.id"), index=True)
    visit_date: Mapped[date] = mapped_column(Date)
    symptom_score: Mapped[int] = mapped_column(Integer)
    outcome: Mapped[str] = mapped_column(String(50))
    notes: Mapped[str] = mapped_column(Text)

    plan: Mapped[FollowupPlan] = relationship(back_populates="records")
