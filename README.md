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

## 本地开发（Conda 方案）

### 1) 初始化 Conda 环境
```bash
conda env create -f environment.yml
conda activate sci-feature
```

### 2) 安装前端依赖
```bash
cd frontend
npm install
```

### 3) 启动服务
```bash
# backend
conda activate sci-feature
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# frontend
conda activate sci-feature
cd frontend
npm run dev -- --hostname 0.0.0.0 --port 3000
```

### 4) 运行测试
```bash
# 离线可运行（不依赖联网安装第三方包）
make test

# 完整 API 测试（依赖 Conda 环境中的 Python 包）
make test-backend-api
```

> 详细说明见 `docs/conda-setup.md`。

## 近期开发任务（按排期）
1. 实现文献导入（DOI + 手动）持久化
2. 实现阅读笔记模板与编辑
3. 接入图谱数据结构与可视化组件
4. 打通“选题子图 -> 综述草稿”工作流

## Week 5 已实现
- 文献导入：支持 `manual` 与 `doi` 两种 source
- PostgreSQL 持久化：`papers` 表与去重索引（标题归一化、DOI 小写唯一）
- Library 页面：可提交文献并实时刷新列表


## Week 6 已实现
- Reader 页面：按文献创建结构化阅读笔记
- 笔记持久化：新增 `notes` 表与按 `paper_id` 查询能力
- Note API：`POST /api/notes`、`GET /api/notes?paper_id=...`
