
from functools import wraps
from server.config.llm_registry import LLM_MAPPER

def inject_llm(llm_key: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            llm = LLM_MAPPER.get(llm_key)
            if not llm:
                raise ValueError(f"LLM with key '{llm_key}' not found in llm_registry")
            kwargs["llm"] = llm
            return await func(*args, **kwargs)
        return wrapper
    return decorator