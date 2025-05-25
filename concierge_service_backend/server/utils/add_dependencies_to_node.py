from functools import partial
from typing import Callable, Any

def add_dependencies_to_node(
    node_func: Callable,
    **kwargs: Any
) -> Callable:
    filtered_kwargs = {k: v for k, v in kwargs.items() if v is not None}
    return partial(node_func, **filtered_kwargs)