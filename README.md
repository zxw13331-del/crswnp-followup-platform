# CRSwNP 术后智能风险分层与随访平台 MVP

本仓库实现第一阶段医学科研概念验证平台，用于展示 CRSwNP 术后模拟病例管理、模拟风险分层、随访节点管理、科研统计与 CSV 导出。

> **重要声明**：本系统仅用于科研概念验证，不可直接用于临床诊疗决策。仓库内置和界面产生的数据均为模拟数据，禁止录入真实姓名、身份证号、手机号、住院号、门诊号等可识别信息，禁止接入 HIS、EMR、PACS、LIS 等真实医疗系统。

## 已实现功能

- React + TypeScript + Vite + Ant Design + ECharts 前端。
- FastAPI + SQLAlchemy + Pydantic 后端。
- SQLite 数据库，启动时自动初始化不少于 60 例模拟患者。
- JSON 配置化模拟风险模型：`backend/app/config/risk_model.json`。
- JSON 配置化术后随访节点：`backend/app/config/followup_schedule.json`。
- 页面：登录页、首页仪表盘、患者列表、新增/编辑患者、患者详情与风险评估、随访管理、科研统计、数据字典。
- CSV 导出：`/api/export/patients.csv`。
- 基础 API 测试与前端构建脚本。

## 演示账号

- 账号：`demo`
- 密码：`demo123`

## 本地启动

### 1. 启动后端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后会自动创建 SQLite 数据库并初始化模拟病例。API 文档地址：<http://127.0.0.1:8000/docs>。

### 2. 启动前端

新开一个终端：

```bash
cd frontend
npm install
npm run dev
```

访问：<http://127.0.0.1:5173>。

## Docker Compose 启动

```bash
docker compose up --build
```

- 前端：<http://127.0.0.1:5173>
- 后端 API：<http://127.0.0.1:8000>
- API 文档：<http://127.0.0.1:8000/docs>

SQLite 数据库通过 Docker volume `backend_data` 持久化。重置演示数据可执行：

```bash
docker compose down -v
```

然后重新 `docker compose up --build`。

## 测试与构建检查

后端测试：

```bash
cd backend
pip install -r requirements.txt
pytest
```

前端构建：

```bash
cd frontend
npm install
npm run build
```

## 后续替换真实研究模型说明

当前风险分层为演示 Logistic 回归，配置文件位于 `backend/app/config/risk_model.json`，版本为 `CRSwNP-DEMO-v0.1`。后续如替换为经过伦理审批和统计验证的真实研究模型，应至少完成：

1. 在 JSON 配置中更新模型版本、变量定义、系数、阈值和免责声明。
2. 在后端 `backend/app/risk.py` 中新增模型输入校验、缺失值策略和版本兼容逻辑。
3. 保留历史 `risk_assessments.model_version`，确保不同模型版本结果可追溯。
4. 增加模型单元测试、边界测试和回归测试。
5. 在界面中明确展示模型来源、适用人群、使用限制和伦理审批状态。
6. 在正式研究环境中替换模拟数据初始化逻辑，并遵循数据脱敏、权限控制和审计要求。

## 文档

- `AGENTS.md`
- `docs/CODEX_TASK.md`
- `docs/MVP_REQUIREMENTS.md`
- `docs/DATA_DICTIONARY.md`
