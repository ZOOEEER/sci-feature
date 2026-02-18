# sci-feature

科研个人工作台（Web）开发中：聚焦文献检索归档、结构化阅读、关系图谱与综述写作。

## 当前进度
- ✅ Phase 0：PRD 与信息架构初稿
- ✅ Phase 1：前后端脚手架
- 🚧 Phase 2：核心功能开发（文献库 + 笔记 + 图谱）

## 项目结构
- `docs/`：产品文档（PRD、IA）
- `frontend/`：Next.js 前端
- `backend/`：FastAPI 后端
- `docker-compose.yml`：本地一键启动依赖服务

## 本地开发

### 1) 后端
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) 前端
```bash
cd frontend
npm install
npm run dev -- --hostname 0.0.0.0 --port 3000
```

### 3) 运行测试
```bash
# 离线可运行（不依赖联网安装第三方包）
make test

# 完整 API 测试（需要先成功安装 backend 依赖）
make test-backend-api
```

## 近期开发任务（按排期）
1. 实现文献导入（DOI + 手动）持久化
2. 实现阅读笔记模板与编辑
3. 接入图谱数据结构与可视化组件
4. 打通“选题子图 -> 综述草稿”工作流
