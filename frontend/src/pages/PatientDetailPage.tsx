import { Button, Card, Descriptions, List, Space, Tag, Typography, message } from 'antd';
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { api, Patient, riskColor, riskLabel, statusLabel } from '../services/api';

export default function PatientDetailPage() {
  const { id } = useParams();
  const [patient, setPatient] = useState<Patient>();
  const load = () => api.get(`/api/patients/${id}`).then(r => setPatient(r.data));
  useEffect(() => {
    void load();
  }, [id]);
  const risk = patient?.risk_assessments[patient.risk_assessments.length - 1];
  const recalc = async () => { await api.post(`/api/patients/${id}/risk-assessment`); message.success('已重新计算模拟风险'); load(); };
  if (!patient) return null;
  return <Space direction="vertical" style={{ width: '100%' }} size="large"><Card title={`患者详情：${patient.demo_code}`} extra={<Link to={`/patients/${patient.id}/edit`}>编辑</Link>}><Descriptions bordered column={3} items={[{ label: '性别', children: patient.sex }, { label: '年龄', children: patient.age }, { label: '手术日期', children: patient.surgery_date }, { label: '哮喘', children: patient.asthma ? '是' : '否' }, { label: '过敏性鼻炎', children: patient.allergic_rhinitis ? '是' : '否' }, { label: '治疗方案', children: patient.treatment_plan }, { label: 'SNOT-22', children: patient.snot22_score }, { label: '鼻息肉评分', children: patient.polyp_score }, { label: '依从性', children: patient.adherence_score }]} /></Card><Card title="风险评估" extra={<Button onClick={recalc}>重新评估</Button>}>{risk && <><Typography.Title level={4}><Tag color={riskColor[risk.risk_level]}>{riskLabel[risk.risk_level]}</Tag>{(risk.probability * 100).toFixed(1)}%</Typography.Title><p>模型版本：{risk.model_version}</p><p>{risk.explanation}</p><div className="warning">{risk.disclaimer}</div></>}</Card><Card title="随访计划"><List dataSource={patient.followup_plans} renderItem={f => <List.Item><List.Item.Meta title={<>{f.title} <Tag>{statusLabel[f.status]}</Tag></>} description={`${f.scheduled_date}｜${f.checklist}`} /></List.Item>} /></Card></Space>;
}
