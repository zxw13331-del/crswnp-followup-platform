import { Card, Select, Table, Tag, Typography } from 'antd';
import { useEffect, useState } from 'react';
import { api, FollowupPlan, statusLabel } from '../services/api';

export default function FollowupsPage() {
  const [rows, setRows] = useState<FollowupPlan[]>([]);
  const [status, setStatus] = useState('');
  useEffect(() => { api.get('/api/followups', { params: { status } }).then(r => setRows(r.data)); }, [status]);
  return <Card><Typography.Title level={3}>随访管理</Typography.Title><Select style={{ width: 160, marginBottom: 16 }} placeholder="状态筛选" allowClear onChange={v => setStatus(v || '')} options={[{ value: 'pending', label: '待随访' }, { value: 'completed', label: '已完成' }, { value: 'overdue', label: '已逾期' }]} /><Table rowKey="id" dataSource={rows} columns={[{ title: '模拟编号', dataIndex: 'demo_code' }, { title: '节点', dataIndex: 'title' }, { title: '计划日期', dataIndex: 'scheduled_date' }, { title: '状态', render: (_: unknown, r: FollowupPlan) => <Tag color={r.status === 'overdue' ? 'red' : r.status === 'completed' ? 'green' : 'blue'}>{statusLabel[r.status]}</Tag> }, { title: '检查项', dataIndex: 'checklist' }]} /></Card>;
}
