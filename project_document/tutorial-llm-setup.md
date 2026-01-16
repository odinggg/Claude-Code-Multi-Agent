# llama.cpp Server 配置教程

本项目使用 llama.cpp server 作为本地 LLM 推理引擎，为 Claude Code 提供快速的代码理解、文档生成和上下文总结能力。

## 快速开始

### 1. 下载并编译 llama.cpp

**macOS/Linux**:
```bash
# 克隆仓库
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp

# 编译（CPU 版本）
make

# 或编译 Metal 加速版本（macOS）
make LLAMA_METAL=1

# 或编译 CUDA 加速版本（NVIDIA GPU）
make LLAMA_CUDA=1
```

**Windows**:
```powershell
# 使用 CMake 编译
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

### 2. 下载模型

推荐使用 GGUF 格式的量化模型：

```bash
# 下载 Gemma 3 1B 模型（约 1GB，推荐轻量使用）
# https://huggingface.co/google/gemma-3-1b-it-gguf

# 下载 Llama 3.2 3B 模型（约 2GB，更好的推理能力）
# https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct-GGUF
```

### 3. 启动 llama.cpp server

```bash
# 基本启动命令
./llama-server -m /path/to/model.gguf --port 8080

# 完整参数示例
./llama-server \
  -m /path/to/gemma-3-1b-it-Q4_K_M.gguf \
  --port 8080 \
  --host 0.0.0.0 \
  --ctx-size 2048 \
  --threads 4

# 使用 GPU 加速（CUDA）
./llama-server \
  -m /path/to/model.gguf \
  --port 8080 \
  --n-gpu-layers 99
```

### 4. 验证服务

```bash
# 测试 API 是否正常
curl http://localhost:8080/health

# 测试推理
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

---

## 项目配置

### 1. 创建环境变量文件

在项目根目录创建 `.env` 文件：

```bash
cp .env.example .env
```

### 2. 配置 LLM 参数

编辑 `.env` 文件：

```bash
# ===== LLM 配置 (llama.cpp server) =====
LLM_MODEL=gemma3:1b
LLM_API_BASE=http://localhost:8080
LLM_TIMEOUT=30
```

### 3. 验证集成

启动 Claude Code 会话，观察是否正常输出项目类型检测结果。

---

## 高级配置

### 使用不同模型

根据硬件配置选择合适的模型：

| 模型 | 显存/内存需求 | 适用场景 |
|------|-------------|---------|
| gemma-3-1b | ~1GB | 轻量开发机 |
| gemma-3-2b | ~2GB | 标准开发机 |
| llama-3.2-3b | ~3GB | 良好推理能力 |
| qwen-2.5-7b | ~8GB | 高质量输出 |

切换模型：
```bash
# 更新 .env 文件
LLM_MODEL=llama-3.2-3b

# 启动对应模型的 server
./llama-server -m /path/to/llama-3.2-3b-instruct.gguf --port 8080
```

### 后台运行

**macOS/Linux**:
```bash
# 使用 nohup 后台运行
nohup ./llama-server -m /path/to/model.gguf --port 8080 &

# 使用 systemd 服务（推荐）
sudo systemctl start llama-server
```

**Windows**:
```powershell
# 使用 PowerShell 后台运行
Start-Process -FilePath ".\llama-server.exe" -ArgumentList "-m", "model.gguf", "--port", "8080" -WindowStyle Hidden
```

---

## 功能说明

配置完成后，项目中的以下功能会自动使用本地 LLM：

1. **项目类型检测** - 会话启动时分析项目结构
2. **用户意图分析** - 判断是否需要使用特定 MCP 工具  
3. **提示词优化** - 自动扩展模糊的开发需求
4. **工具安全分析** - 检测高风险操作
5. **知识提取** - 会话结束时提取可复用知识
6. **上下文摘要** - 压缩长对话上下文

---

## 常见问题

### Q1: Server 无法启动？

```bash
# 检查端口是否被占用
lsof -i :8080

# 检查模型文件是否存在
ls -l /path/to/model.gguf

# 查看详细日志
./llama-server -m /path/to/model.gguf --port 8080 -v
```

### Q2: API 返回 502 错误？

Server 可能正在加载模型，等待几秒后重试。或检查：
- 模型路径是否正确
- 是否有足够的内存/显存

### Q3: 响应速度太慢？

- 使用更小的量化版本（Q4_K_M vs Q8）
- 减少 `--ctx-size` 参数
- 使用 GPU 加速

### Q4: 如何查看日志？

```bash
# server 启动时添加 -v 参数
./llama-server -m /path/to/model.gguf --port 8080 -v

# 或查看 hooks 日志
cat logs/hooks_$(date +%Y%m%d).log
```

---

## 从 Ollama 迁移

如果之前使用 Ollama，迁移步骤：

1. **环境变量**：旧的 `OLLAMA_MODEL` 和 `OLLAMA_API_BASE` 仍然有效，会自动映射
2. **模型名称**：保持使用相同的模型名称（如 `gemma3:1b`）
3. **API 端点**：更新 `LLM_API_BASE` 为 llama.cpp server 地址

---

## 参考资源

- [llama.cpp 官方仓库](https://github.com/ggerganov/llama.cpp)
- [llama.cpp server 文档](https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md)
- [GGUF 模型库](https://huggingface.co/models?search=gguf)
