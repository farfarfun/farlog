# Changelog

## 1.1.9（未发布）

### 新增

- `src/farlog/py.typed` 标记文件，并在打包配置中声明收录，下游可直接获得类型信息（PEP 561）。
- `[dependency-groups].dev` 开发依赖组（`pytest`、`ruff`），测试与静态检查命令统一走 `uv run`。

### 修复

- README 环境要求与 `pyproject.toml` `requires-python`/Ruff `target-version` 不一致（README 写 3.9，实际要求 3.10），统一为 Python 3.10。
- `configure()`/`get_logger()` 补充中文 docstring（说明参数、返回值）与 `get_logger()` 返回类型标注。
- README 的测试命令此前依赖未声明的全局 `pytest`，在干净环境中无法执行。

### 变更

- 构建后端迁移到 Hatchling，`[tool.hatch.build.targets.wheel]` 显式声明打包目录。
- `requires-python` 下限提升到 `>=3.10`（3.9 已 EOL）。
- 补齐 `license-files`、作者/维护者与项目 URL 等打包元信息。
- README 末尾追加组织介绍固定区块。
- `.gitignore` 补充 `*.db`、`*.rar`、`.run/`、`.idea/`、`.vscode/` 规则。
- 本文件改为按版本倒序、每版四类分类维护。

### 废弃

（无）

## 1.1.8 - 2026-08-27

### 新增

（无）

### 修复

（无）

### 变更

- 版本号发布性递增，内容同 1.1.7；同时把仓库 URL 元信息更新为 `farfarfun/farlog`。

### 废弃

（无）

## 1.1.7 - 2026-08-26

### 新增

- 以 `farlog` 为包名发布的首个版本，导入路径为 `farlog`。

### 修复

（无）

### 变更

- **破坏性变更**：分发包名与导入路径由旧包名改为 `farlog`。
  迁移方法：安装 `farlog>=1.1.7`，并把 `import` 语句中的旧包名替换为 `farlog`；
  `configure()` / `get_logger()` / `getLogger()` 的签名与行为保持不变，除包名外无需改动调用代码。

### 废弃

- 旧包名不再接收更新，请统一迁移到 `farlog`。

## 1.1.7 之前的版本

1.1.7 之前的发布使用的是旧包名，未在 PyPI 的 `farlog` 项目下发布，也没有维护 CHANGELOG。
根据 git 历史，这些版本的主要变更为：

- **1.1.4（2026-08-03）**：重写 `core.py`；`get_logger(name)` 增加名称校验，含路径分隔符或 `..` 的名称抛 `ValueError`；
  `configure()` 支持切换日志目录并迁移已创建的命名 handler；补充 README 与 `tests/`。
- **1.1.5 / 1.1.6（2026-08-03）**：仅版本号递增，无功能变更。
- **1.1.1 - 1.1.3（2026-03-16）**：包名与版本号调整，`uv.lock` 一度被移除。
- **0.1.x - 1.0.x（2026-02 - 2026-02-24）**：早期迭代，按名称拆分日志文件、按日轮转与压缩等基础能力成型。
