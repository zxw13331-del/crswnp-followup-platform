# 数据字典

## patients
| 字段 | 含义 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| research_code | 科研编号 | string | 是 | 仅使用脱敏编号，如 CRS-2026-0001 |
| age | 年龄 | integer | 是 | 18-90 |
| sex | 性别 | enum | 是 | male / female |
| bmi | BMI | float | 否 | kg/m² |
| disease_duration_years | 病程年限 | float | 否 | 年 |
| smoking_history | 吸烟史 | boolean | 否 | true / false |
| asthma | 哮喘史 | boolean | 否 | true / false |
| allergic_rhinitis | 变应性鼻炎 | boolean | 否 | true / false |
| aspirin_intolerance | 阿司匹林不耐受 | boolean | 否 | true / false |
| previous_sinus_surgeries | 既往鼻窦手术次数 | integer | 否 | >=0 |
| eos_count | 嗜酸性粒细胞计数 | float | 否 | 统一单位 |
| eos_percent | 嗜酸性粒细胞比例 | float | 否 | 0-100 |
| total_ige | 总 IgE | float | 否 | IU/mL |
| lund_mackay_score | Lund–Mackay 评分 | integer | 否 | 0-24 |
| nasal_polyp_score | 鼻息肉评分 | integer | 否 | 0-8 |
| lund_kennedy_score | Lund–Kennedy 评分 | integer | 否 | 按预设范围校验 |
| mucosal_edema | 黏膜水肿 | boolean | 否 | true / false |
| purulent_discharge | 脓性分泌物 | boolean | 否 | true / false |
| snot22_score | SNOT-22 评分 | integer | 否 | 0-110 |
| nasal_obstruction_score | 鼻塞视觉评分 | integer | 否 | 0-10 |
| olfactory_decline_level | 嗅觉下降程度 | enum | 否 | none / mild / moderate / severe |
| surgery_date | 手术日期 | date | 是 | YYYY-MM-DD |
| local_steroid_delivery_method | 局部糖皮质激素递送方式 | enum | 否 | spray / high_volume_irrigation / other |
| irrigation_method | 鼻腔冲洗方式 | string | 否 | 脱敏描述 |
| medication_adherence | 用药依从性 | enum | 否 | good / fair / poor |

## risk_assessments
| 字段 | 含义 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| patient_id | 患者 ID | integer | 是 | 外键 |
| risk_probability | 风险概率 | float | 是 | 0-1 |
| risk_level | 风险等级 | enum | 是 | low / medium / high |
| model_version | 模型版本 | string | 是 | CRSwNP-DEMO-v0.1 |
| major_risk_factors_json | 主要风险因素 | json | 是 | 模拟解释数据 |

## followup_plans
| 字段 | 含义 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| patient_id | 患者 ID | integer | 是 | 外键 |
| planned_date | 计划随访日期 | date | 是 | YYYY-MM-DD |
| followup_stage | 随访阶段 | string | 是 | 2w / 1m / 3m / 6m / 9m / 12m |
| status | 状态 | enum | 是 | pending / completed / overdue |

## followup_records
| 字段 | 含义 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| followup_plan_id | 随访计划 ID | integer | 是 | 外键 |
| actual_date | 实际随访日期 | date | 是 | YYYY-MM-DD |
| nasal_polyp_score | 鼻息肉评分 | integer | 否 | 0-8 |
| lund_kennedy_score | Lund–Kennedy 评分 | integer | 否 | 按预设范围校验 |
| snot22_score | SNOT-22 评分 | integer | 否 | 0-110 |
| olfactory_change | 嗅觉变化 | enum | 否 | improved / stable / worsened |
| systemic_steroid_used | 使用系统性糖皮质激素 | boolean | 否 | true / false |
| revision_surgery | 再次手术 | boolean | 否 | true / false |
| delivery_method_adjusted | 调整递送方式 | boolean | 否 | true / false |
| medication_adherence | 用药依从性 | enum | 否 | good / fair / poor |
| notes | 医生备注 | string | 否 | 禁止写入可识别身份信息 |
