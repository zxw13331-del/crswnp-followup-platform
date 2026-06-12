import { Button, Card, DatePicker, Form, InputNumber, Select, Switch, message } from 'antd';
import dayjs from 'dayjs';
import { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { api } from '../services/api';

export default function PatientFormPage() {
  const [form] = Form.useForm();
  const { id } = useParams();
  const navigate = useNavigate();
  useEffect(() => { if (id) api.get(`/api/patients/${id}`).then(({ data }) => form.setFieldsValue({ ...data, surgery_date: dayjs(data.surgery_date) })); }, [id, form]);
  const onFinish = async (values: any) => {
    const payload = { ...values, surgery_date: values.surgery_date.format('YYYY-MM-DD') };
    const res = id ? await api.put(`/api/patients/${id}`, payload) : await api.post('/api/patients', payload);
    message.success('已保存模拟患者并完成风险评估');
    navigate(`/patients/${res.data.id}`);
  };
  return <Card title={id ? '编辑模拟患者' : '新增模拟患者'}><Form form={form} layout="vertical" onFinish={onFinish} initialValues={{ sex: '女', age: 45, surgery_date: dayjs(), asthma: false, allergic_rhinitis: false, prior_surgery_count: 0, eosinophil_percent: 5, tissue_eosinophil_level: 1, snot22_score: 40, polyp_score: 4, adherence_score: 0.7, treatment_plan: '鼻喷雾 + 大容量鼻腔冲洗' }}><Form.Item label="性别" name="sex"><Select options={[{ value: '男' }, { value: '女' }]} /></Form.Item><Form.Item label="年龄" name="age"><InputNumber min={18} max={85} /></Form.Item><Form.Item label="手术日期" name="surgery_date"><DatePicker /></Form.Item><Form.Item label="合并哮喘" name="asthma" valuePropName="checked"><Switch /></Form.Item><Form.Item label="合并过敏性鼻炎" name="allergic_rhinitis" valuePropName="checked"><Switch /></Form.Item><Form.Item label="既往手术次数" name="prior_surgery_count"><InputNumber min={0} max={5} /></Form.Item><Form.Item label="外周血嗜酸细胞比例（%）" name="eosinophil_percent"><InputNumber min={0} max={30} step={0.1} /></Form.Item><Form.Item label="组织嗜酸水平（0-3）" name="tissue_eosinophil_level"><InputNumber min={0} max={3} /></Form.Item><Form.Item label="SNOT-22 模拟分" name="snot22_score"><InputNumber min={0} max={110} /></Form.Item><Form.Item label="鼻息肉评分" name="polyp_score"><InputNumber min={0} max={8} /></Form.Item><Form.Item label="依从性评分" name="adherence_score"><InputNumber min={0} max={1} step={0.05} /></Form.Item><Form.Item label="治疗方案" name="treatment_plan"><Select options={[{ value: '鼻喷雾' }, { value: '大容量鼻腔冲洗' }, { value: '鼻喷雾 + 大容量鼻腔冲洗' }]} /></Form.Item><Button type="primary" htmlType="submit">保存</Button></Form></Card>;
}
