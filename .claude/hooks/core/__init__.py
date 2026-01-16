"""
Hooks Core 模块
提供基础类和工具
"""
from .base_hook import BaseHook, HookResult
from .config import config
from .logger import logger
from .llm_client import llm, ollama  # LLM 客户端（向后兼容 ollama 别名）
from .document_manager import DocumentManager

__all__ = ['config', 'logger', 'llm', 'ollama', 'BaseHook', 'HookResult', 'DocumentManager']
