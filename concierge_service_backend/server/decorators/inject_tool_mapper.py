from functools import wraps
from typing import List, Callable
from langchain_core.tools import Tool
from server.utils.tool_str_to_func import tool_str_func_mapping

def inject_tool_mapping(tools: List[Tool]):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tool_map = tool_str_func_mapping(tools)
            kwargs['tools'] = tool_map
            return await func(*args, **kwargs)
        return wrapper
    return decorator