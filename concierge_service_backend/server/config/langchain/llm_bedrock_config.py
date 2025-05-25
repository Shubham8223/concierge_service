from pydantic import BaseModel, Field
from enum import Enum

class ModelId(str, Enum):
    CLAUDE_3_HAIKU = "us.anthropic.claude-3-haiku-20240307-v1:0"
    CLAUDE_3_SONNET = "us.anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_3_OPUS = "us.anthropic.claude-3-opus-20240229-v1:0",
    CLAUDE_3_5_SONNET ="us.anthropic.claude-3-5-sonnet-20240620-v1:0"
    CLAUDE_3_7_SONNET ="us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    LLAMA_3_3_70B ="us.meta.llama3-3-70b-instruct-v1:0"
    

class ModelKwargsClaude(BaseModel):
    temperature: float = Field(default=0.1, ge=0, le=1)
    max_tokens: int = Field(default=2048, ge=1, le=4096)
    top_p: float = Field(default=0.999, ge=0, le=1)
    top_k: int = Field(default=0, ge=0, le=500)
    
class ModelKwargsLlama(BaseModel):
    temperature: float = Field(default=0.1, ge=0, le=1)
    max_tokens: int = Field(default=2048, ge=1, le=4096)
    top_p: float = Field(default=0.999, ge=0, le=1)