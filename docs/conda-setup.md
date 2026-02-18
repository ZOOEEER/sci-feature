# Conda 开发环境方案

本项目推荐使用 Conda 统一管理 Python + Node.js 依赖，避免 venv 与系统 Node 版本不一致。

## 1) 初始化环境

```bash
conda env create -f environment.yml
conda activate sci-feature
```

## 2) 安装前端依赖

> Node.js 由 Conda 提供，npm 也在同一环境中。

```bash
cd frontend
npm install
```

## 3) 启动服务

### 后端
```bash
conda activate sci-feature
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端
```bash
conda activate sci-feature
cd frontend
npm run dev -- --hostname 0.0.0.0 --port 3000
```

## 4) 测试

```bash
# 离线测试（不依赖第三方包）
make test

# 完整 API 测试（依赖 Conda 环境中的 Python 包）
make test-backend-api
```

## 5) 更新环境

当 `environment.yml` 变更后执行：

```bash
conda env update -f environment.yml --prune
```
