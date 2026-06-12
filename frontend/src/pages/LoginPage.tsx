import { Button, Card, Form, Input, Typography, message } from 'antd';
import { useNavigate } from 'react-router-dom';
import { api } from '../services/api';

export default function LoginPage() {
  const navigate = useNavigate();
  const onFinish = async (values: { username: string; password: string }) => {
    try {
      const { data } = await api.post('/api/auth/login', values);
      localStorage.setItem('demo-token', data.token);
      message.success('登录成功');
      navigate('/');
    } catch {
      message.error('请使用演示账号 demo / demo123');
    }
  };
  return <div className="login-page"><Card className="login-card"><Typography.Title level={3}>CRSwNP 科研演示登录</Typography.Title><Typography.Paragraph>演示账号：demo / demo123</Typography.Paragraph><Form layout="vertical" initialValues={{ username: 'demo', password: 'demo123' }} onFinish={onFinish}><Form.Item label="账号" name="username"><Input /></Form.Item><Form.Item label="密码" name="password"><Input.Password /></Form.Item><Button type="primary" htmlType="submit" block>进入平台</Button></Form></Card></div>;
}
