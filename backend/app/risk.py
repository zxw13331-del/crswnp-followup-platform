import json
import math
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config" / "risk_model.json"


def load_risk_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def calculate_risk(patient) -> dict:
    cfg = load_risk_config()
    coef = cfg["coefficients"]
    z = cfg["intercept"]
    z += coef["age"] * patient.age
    z += coef["eosinophil_percent"] * patient.eosinophil_percent
    z += coef["tissue_eosinophil_level"] * patient.tissue_eosinophil_level
    z += coef["asthma"] * int(patient.asthma)
    z += coef["allergic_rhinitis"] * int(patient.allergic_rhinitis)
    z += coef["prior_surgery_count"] * patient.prior_surgery_count
    z += coef["snot22_score"] * patient.snot22_score
    z += coef["polyp_score"] * patient.polyp_score
    z += coef["adherence_score"] * patient.adherence_score
    probability = 1 / (1 + math.exp(-z))
    thresholds = cfg["thresholds"]
    if probability < thresholds["low_max"]:
        risk_level = "low"
    elif probability < thresholds["medium_max"]:
        risk_level = "medium"
    else:
        risk_level = "high"
    explanation = (
        f"模拟 Logistic 回归得分 {z:.2f}；主要输入包含嗜酸细胞比例、组织嗜酸水平、"
        f"哮喘/过敏性鼻炎、既往手术次数、SNOT-22、鼻息肉评分与依从性。"
    )
    return {
        "model_version": cfg["model_version"],
        "probability": round(probability, 4),
        "risk_level": risk_level,
        "explanation": explanation,
        "disclaimer": cfg["disclaimer"],
    }
