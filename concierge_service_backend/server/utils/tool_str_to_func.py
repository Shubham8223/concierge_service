from typing import List, Dict, Callable, Any
from langchain_core.tools import Tool

def tool_str_func_mapping(tools: List[Tool]) -> Dict[str, Tool]:
    tool_func_dict = {}
    for tool in tools:
        tool_func_dict[tool.name] = tool
    return tool_func_dict