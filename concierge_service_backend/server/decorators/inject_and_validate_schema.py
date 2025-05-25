from functools import wraps
from typing import Callable, Union, Type

def inject_and_validate_schema(schema_or_getter: Union[Callable, Type]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                if callable(schema_or_getter) and not isinstance(schema_or_getter, type):
                    schema_class_and_other_kwargs = schema_or_getter(*args, **kwargs)
                    schema_class = schema_class_and_other_kwargs["schema_class"]
                    kwargs.update(schema_class_and_other_kwargs)
                else:
                    schema_class = schema_or_getter
                    kwargs['schema_class'] = schema_class
                result = await func(*args, **kwargs)
                schema_class.model_validate(result)
                return result

            except Exception as e:
                print("Validation error:", e)
                raise RuntimeError(f"Response validation failed: {str(e)}")
        return wrapper
    return decorator