import hashlib
import json
from fastapi import Request, Response
from functools import wraps
from server.config.redis import get_value, set_value
from server.config.config import Settings
from typing import Callable 

def cache_check_decorator(func : Callable):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        ttl_value = Settings.REDIS_TTL
        params = json.dumps(request.path_params)
        body = await request.body()
        body_str = body.decode() if body else ''
        hash_input = params + body_str
        hash_key = hashlib.sha256(hash_input.encode('utf-8')).hexdigest() # hashing payload for key compression via SHA
        last_path_segment = request.url.path.split("/")[-1]
        redis_key = f"{last_path_segment}:{hash_key}"
        if request.method in ["GET", "POST"]: # condition for caching hit
            try:
                cached_data = await get_value(redis_key)
                if cached_data:
                    print(f"Cache hit for key: {redis_key}")
                    return Response(content=cached_data, media_type="application/json")
            except Exception as err:
                print(f"Error fetching from Redis: {err}")
        
        response = await func(request, *args, **kwargs)

        if redis_key and response:   # condition for caching setting
            await set_value(redis_key, response.body, ttl=ttl_value) 
        return response

    return wrapper
