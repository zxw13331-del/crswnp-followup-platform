import { Button, Card, Input, Select, Space, Table, Tag, Typography } from 'antd';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api, Patient, riskColor, riskLabel } from '../services/api';

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [q, setQ] = useState('');
  const [risk, setRisk] = useState('');
  const load = () => api.get('/api/patients', { params: { q, risk_level: risk } }).then(r => setPatients(r.data));
  useEffect(load, [q, risk]);
  const columns = [
    { title: '模拟编号', dataIndex: 'demo_code' }, { title: '性别', dataIndex: 'sex' }, { title: '年龄', dataIndex: 'age' }, { title: '手术日期', dataIndex: 'surgery_date' },
    { title: '风险', render: (_: unknown, p: Patient) => { const r = p.risk_assessments[p.risk_assessments.length - 1]; return r ? <Tag color={riskColor[r.risk_level]}>{riskLabel[r.risk_level]} {(r.probability * 100).toFixed(1)}%</Tag> : '-'; } },
    { title: '治疗方案', dataIndex: 'treatment_plan' },
    { title: '操作', render: (_: unknown, p: Patient) => <Space><Link to={`/patients/${p.id}`}>详情/评估</Link><Link to={`/patients/${p.id}/edit`}>编辑</Link></Space> }
  ];
  return <Card><Space style={{ marginBottom: 16 }}><Typography.Title level={3} style={{ margin: 0 }}>患者列表</Typography.Title><Input.Search placeholder="搜索模拟编号" onSearch={setQ} allowClear /><Select style={{ width: 140 }} placeholder="风险筛选" allowClear onChange={v => setRisk(v || '')} options={[{ value: 'low', label: '低风险' }, { value: 'medium', label: '中风险' }, { value: 'high', label: '高风险' }]} /><Button type="primary" href="/api/export/patients.csv">导出 CSV</Button><Link to="/patients/new"><Button>新增模拟患者</Button></Link></Space><Table rowKey="id" columns={columns} dataSource={patients} /></Card>;
}
