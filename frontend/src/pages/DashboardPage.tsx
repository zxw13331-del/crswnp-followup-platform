import { Card, Statistic, Typography } from 'antd';
import ReactECharts from 'echarts-for-react';
import { useEffect, useState } from 'react';
import { api, riskLabel, statusLabel } from '../services/api';

export default function DashboardPage() {
  const [data, setData] = useState<any>();
  useEffect(() => { api.get('/api/dashboard').then(r => setData(r.data)); }, []);
  const risk = Object.entries(data?.risk_counts || {}).map(([name, value]) => ({ name: riskLabel[name] || name, value }));
  const follow = Object.entries(data?.followup_counts || {}).map(([name, value]) => ({ name: statusLabel[name] || name, value }));
  return <><Typography.Title level={3}>首页仪表盘</Typography.Title><div className="card-grid"><Card><Statistic title="模拟患者总数" value={data?.total_patients || 0} /></Card><Card><Statistic title="高风险病例" value={data?.risk_counts?.high || 0} /></Card><Card><Statistic title="待随访节点" value={data?.followup_counts?.pending || 0} /></Card><Card><Statistic title="已逾期节点" value={data?.followup_counts?.overdue || 0} /></Card></div><Card title="风险与随访概览"><ReactECharts option={{ tooltip: {}, legend: {}, series: [{ name: '风险分层', type: 'pie', radius: '50%', data: risk }, { name: '随访状态', type: 'pie', radius: '50%', center: ['75%', '50%'], data: follow }] }} style={{ height: 360 }} /></Card></>;
}
