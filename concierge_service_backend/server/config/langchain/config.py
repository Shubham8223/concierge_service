from langchain_aws.chat_models import ChatBedrock
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from mypy_boto3_bedrock_runtime.client import BedrockRuntimeClient
from server.config.langchain import llm_bedrock_config,llm_together_config,llm_groq_config
from langchain_together import ChatTogether
from langchain_groq import ChatGroq
from typing import Union
from server.config.config import settings


def get_bedrock_model(
  client: BedrockRuntimeClient,
  model_id: llm_bedrock_config.ModelId,
  model_kwargs: Union[llm_bedrock_config.ModelKwargsClaude,llm_bedrock_config.ModelKwargsLlama],
  streaming: bool = False,
  verbose: bool = False) -> ChatBedrock:
    return ChatBedrock(
        client=client,
        model_id=model_id.value,
        model_kwargs=model_kwargs.__dict__,
        streaming=streaming,
        verbose=verbose,
        callbacks=[StreamingStdOutCallbackHandler()] if streaming else []
    )
    
def get_together_model( 
  model_id: llm_together_config.ModelId,
  model_kwargs: llm_together_config.ModelKwargs,
  streaming: bool = False,
  verbose: bool = False) -> ChatTogether:
    return ChatTogether(
      together_api_key = settings.TOGETHER_API_KEY,
      model=model_id,
      model_kwargs=model_kwargs.__dict__,
      streaming=streaming,
      verbose=verbose,
      callbacks=[StreamingStdOutCallbackHandler()] if streaming else []
      )
    
def get_groq_model( 
  model_id: llm_groq_config.ModelId,
  model_kwargs: llm_groq_config.ModelKwargs,
  streaming: bool = False,
  verbose: bool = False) -> ChatGroq:
    return ChatGroq(
      groq_api_key = settings.GROQ_API_KEY,
      model=model_id,
      model_kwargs=model_kwargs.__dict__,
      streaming=streaming,
      verbose=verbose,
      callbacks=[StreamingStdOutCallbackHandler()] if streaming else []
      )