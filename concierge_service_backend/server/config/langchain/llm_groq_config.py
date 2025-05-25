from pydantic import BaseModel, Field
from enum import Enum

class ModelId(str, Enum):
    LLAMA_3_3_70B = "llama-3.3-70b-versatile"
    
class ModelKwargs(BaseModel):
    temperature: float = Field(default=0.1, ge=0, le=1)
    max_tokens: int = Field(default=2048, ge=1, le=4096)
    top_p: float = Field(default=0.999, ge=0, le=1)