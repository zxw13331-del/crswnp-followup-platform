import { Card, Typography } from 'antd';
import ReactECharts from 'echarts-for-react';
import { useEffect, useState } from 'react';
import { api, riskLabel, statusLabel } from '../services/api';

export default function StatsPage() {
  const [data, setData] = useState<any>();
  useEffect(() => { api.get('/api/stats').then(r => setData(r.data)); }, []);
  const risk = (data?.risk_distribution || []).map((x: any) => ({ ...x, name: riskLabel[x.name] || x.name }));
  const follow = (data?.followup_status_distribution || []).map((x: any) => ({ ...x, name: statusLabel[x.name] || x.name }));
  return <><Typography.Title level={3}>科研统计</Typography.Title><Card title="分布统计"><ReactECharts style={{ height: 420 }} option={{ tooltip: {}, legend: {}, xAxis: [{ type: 'category', data: (data?.average_scores_by_risk || []).map((x: any) => riskLabel[x.risk_level]) }], yAxis: [{ type: 'value' }], series: [{ name: '风险分布', type: 'pie', radius: '35%', center: ['20%', '40%'], data: risk }, { name: '随访状态', type: 'pie', radius: '35%', center: ['52%', '40%'], data: follow }, { name: '平均 SNOT-22', type: 'bar', data: (data?.average_scores_by_risk || []).map((x: any) => x.snot22) }] }} /></Card><Card title="模拟随访结局" style={{ marginTop: 16 }}><ReactECharts style={{ height: 300 }} option={{ tooltip: {}, xAxis: { type: 'category', data: (data?.outcome_distribution || []).map((x: any) => x.name) }, yAxis: { type: 'value' }, series: [{ type: 'bar', data: (data?.outcome_distribution || []).map((x: any) => x.value) }] }} /></Card></>;
}
