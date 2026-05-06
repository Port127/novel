#!/usr/bin/env python
"""统一 LLM 调用客户端。

特性：
- 指数退避自动重试（网络超时、限流、服务端 5xx）
- 429 速率限制处理
- Token 统计
"""
import sys
import json
import logging
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# 简单日志配置
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# 全局 API 调用计数器
_api_stats = {"calls": 0, "errors": 0, "tokens_total": 0}


def get_api_stats() -> dict:
    """获取全局 API 调用统计（只读快照）。"""
    return dict(_api_stats)


def reset_api_stats() -> None:
    """重置计数器。"""
    _api_stats["calls"] = 0
    _api_stats["errors"] = 0
    _api_stats["tokens_total"] = 0


def load_config():
    """从环境变量加载 LLM 配置。"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    import os
    return {
        "llm": {
            "model": os.getenv("LLM_MODEL", "gpt-4o-mini"),
            "api_key": os.getenv("LLM_API_KEY", ""),
            "base_url": os.getenv("LLM_API_BASE"),
            "max_tokens": int(os.getenv("LLM_MAX_TOKENS", "2048")),
            "temperature": float(os.getenv("LLM_TEMPERATURE", "0.7")),
            "timeout_seconds": int(os.getenv("LLM_TIMEOUT_SECONDS", "120")),
        }
    }


def truncate_to_tokens(text: str, max_tokens: int, model: str = "gpt-4o-mini") -> str:
    """将文本截断到指定 Token 数量上限。"""
    try:
        import tiktoken
        try:
            enc = tiktoken.encoding_for_model(model)
        except KeyError:
            enc = tiktoken.get_encoding("cl100k_base")

        tokens = enc.encode(text)
        if len(tokens) <= max_tokens:
            return text
        truncated_tokens = tokens[:max_tokens]
        return enc.decode(truncated_tokens)
    except ImportError:
        # 回退：中文平均 1 token ≈ 1.5 字符
        char_limit = int(max_tokens * 1.5)
        return text[:char_limit]


def _retry_wait(retry_state) -> float:
    """自适应等待策略：429 优先读取 Retry-After 头，其他错误指数退避。"""
    from openai import APIStatusError
    exc = retry_state.outcome.exception()

    if isinstance(exc, APIStatusError) and exc.status_code == 429:
        headers = {}
        try:
            headers = dict(exc.response.headers) if exc.response else {}
        except Exception:
            pass

        for header in ("retry-after", "x-ratelimit-reset-requests"):
            val = headers.get(header) or headers.get(header.lower())
            if val:
                try:
                    wait = float(val)
                    logger.warning(f"速率限制（429），等待 {wait:.0f}s")
                    return wait
                except (TypeError, ValueError):
                    pass

        logger.warning("速率限制（429），默认等待 30s")
        return 30.0

    # 其他错误：指数退避，上限 60s
    wait = min(2 ** retry_state.attempt_number, 60)
    return wait


def call_llm(
    system_prompt: str,
    user_prompt: str,
    config: dict = None,
    max_tokens_override: int = None,
    timeout_override: int = None,
    json_response: bool = True,
) -> str | dict:
    """调用 LLM API。

    Args:
        system_prompt: 系统提示词
        user_prompt: 用户提示词
        config: 配置字典（None 时自动加载）
        max_tokens_override: 可选，覆盖 max_tokens
        timeout_override: 可选，覆盖 timeout
        json_response: 是否要求 JSON 格式返回

    Returns:
        str | dict: LLM 返回内容（JSON 格式时返回 dict）

    Raises:
        ValueError: API_KEY 未配置
        openai.APIError: 超过最大重试次数后仍失败
    """
    from openai import OpenAI, APIStatusError, APIConnectionError, APITimeoutError
    from tenacity import (
        retry,
        stop_after_attempt,
        retry_if_exception_type,
        before_sleep_log,
    )

    if config is None:
        config = load_config()

    if not config["llm"]["api_key"]:
        raise ValueError("LLM_API_KEY 未配置，请检查 .env 文件")

    effective_max_tokens = max_tokens_override or config["llm"].get("max_tokens", 2048)
    effective_timeout = timeout_override or config["llm"].get("timeout_seconds", 120)

    @retry(
        retry=retry_if_exception_type((APIConnectionError, APITimeoutError, APIStatusError)),
        stop=stop_after_attempt(5),
        wait=_retry_wait,
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def _call() -> str:
        client = OpenAI(
            api_key=config["llm"]["api_key"],
            base_url=config["llm"].get("base_url"),
        )

        request_params = {
            "model": config["llm"]["model"],
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": config["llm"].get("temperature", 0.7),
            "max_tokens": effective_max_tokens,
            "timeout": effective_timeout,
        }

        if json_response:
            request_params["response_format"] = {"type": "json_object"}

        response = client.chat.completions.create(**request_params)
        usage = response.usage
        _api_stats["calls"] += 1
        if usage:
            _api_stats["tokens_total"] += usage.total_tokens

        return response.choices[0].message.content

    try:
        result = _call()
        if json_response:
            return json.loads(result)
        return result
    except Exception:
        _api_stats["errors"] += 1
        raise


def call_llm_simple(prompt: str, system_prompt: str = None, config: dict = None) -> str:
    """简化版 LLM 调用（非 JSON 格式）。

    Args:
        prompt: 用户提示词
        system_prompt: 系统提示词（可选）
        config: 配置字典

    Returns:
        str: LLM 返回文本
    """
    if system_prompt is None:
        system_prompt = "你是一个专业的小说写作助手。"
    return call_llm(
        system_prompt=system_prompt,
        user_prompt=prompt,
        config=config,
        json_response=False,
    )