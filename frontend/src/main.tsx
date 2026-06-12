import React from 'react';
import ReactDOM from 'react-dom/client';
import { HashRouter, Navigate, Route, Routes, useNavigate } from 'react-router-dom';
import { App as AntApp, Button, Layout, Menu, Typography } from 'antd';
import 'antd/dist/reset.css';
import './style.css';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import PatientsPage from './pages/PatientsPage';
import PatientFormPage from './pages/PatientFormPage';
import PatientDetailPage from './pages/PatientDetailPage';
import FollowupsPage from './pages/FollowupsPage';
import StatsPage from './pages/StatsPage';
import DictionaryPage from './pages/DictionaryPage';

const { Header, Content, Sider } = Layout;

function Shell() {
  const navigate = useNavigate();
  const token = localStorage.getItem('demo-token');
  if (!token) return <Navigate to="/login" replace />;
  const items = [
    { key: '/', label: '首页仪表盘' },
    { key: '/patients', label: '患者列表' },
    { key: '/patients/new', label: '新增模拟患者' },
    { key: '/followups', label: '随访管理' },
    { key: '/stats', label: '科研统计' },
    { key: '/dictionary', label: '数据字典' }
  ];
  return (
    <Layout className="app-shell">
      <Sider width={220} theme="light">
        <div className="logo">CRSwNP 科研随访</div>
        <Menu mode="inline" items={items} onClick={({ key }) => navigate(key)} />
      </Sider>
      <Layout>
        <Header className="topbar">
          <Typography.Text strong>术后智能风险分层与随访平台（演示）</Typography.Text>
          <Button onClick={() => { localStorage.removeItem('demo-token'); navigate('/login'); }}>退出</Button>
        </Header>
        <Content className="content">
          <div className="warning">仅用于科研概念验证，不可直接用于临床诊疗决策；请勿录入任何真实可识别医疗信息。</div>
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/patients" element={<PatientsPage />} />
            <Route path="/patients/new" element={<PatientFormPage />} />
            <Route path="/patients/:id/edit" element={<PatientFormPage />} />
            <Route path="/patients/:id" element={<PatientDetailPage />} />
            <Route path="/followups" element={<FollowupsPage />} />
            <Route path="/stats" element={<StatsPage />} />
            <Route path="/dictionary" element={<DictionaryPage />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AntApp>
      <HashRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/*" element={<Shell />} />
        </Routes>
      </HashRouter>
    </AntApp>
  </React.StrictMode>
);
