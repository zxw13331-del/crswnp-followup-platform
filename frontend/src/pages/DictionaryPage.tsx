import { Card, Table, Typography } from 'antd';
import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function DictionaryPage() {
  const [data, setData] = useState<any>({ fields: [] });
  useEffect(() => { api.get('/api/dictionary').then(r => setData(r.data)); }, []);
  return <Card><Typography.Title level={3}>数据字典</Typography.Title><Typography.Paragraph>{data.privacy_notice}</Typography.Paragraph><Table rowKey="name" dataSource={data.fields} columns={[{ title: '字段', dataIndex: 'name' }, { title: '中文名称', dataIndex: 'label' }, { title: '说明', dataIndex: 'description' }]} /></Card>;
}
