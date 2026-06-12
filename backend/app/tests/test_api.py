import os
import tempfile

fd, db_path = tempfile.mkstemp(suffix=".db")
os.close(fd)
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

client = TestClient(app)


def test_health_and_seeded_dashboard():
    with client:
        health = client.get("/api/health")
        assert health.status_code == 200
        dashboard = client.get("/api/dashboard")
        assert dashboard.status_code == 200
        data = dashboard.json()
        assert data["total_patients"] >= 60
        assert "仅用于科研概念验证" in data["disclaimer"]


def test_patients_and_risk_assessment():
    with client:
        patients = client.get("/api/patients").json()
        assert len(patients) >= 60
        patient_id = patients[0]["id"]
        risk = client.post(f"/api/patients/{patient_id}/risk-assessment")
        assert risk.status_code == 200
        assert risk.json()["risk_level"] in {"low", "medium", "high"}


def test_followups_stats_dictionary_and_csv():
    with client:
        assert client.get("/api/followups").status_code == 200
        stats = client.get("/api/stats")
        assert stats.status_code == 200
        assert stats.json()["risk_distribution"]
        dictionary = client.get("/api/dictionary")
        assert dictionary.status_code == 200
        assert dictionary.json()["fields"]
        csv_response = client.get("/api/export/patients.csv")
        assert csv_response.status_code == 200
        assert "demo_code" in csv_response.text
