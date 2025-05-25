from server.config.bedrock import get_bedrock_client
from server.config.langchain.config import get_bedrock_model 
from server.config.langchain import llm_bedrock_config


client = get_bedrock_client()

bedrock_llama_3_3 = get_bedrock_model( client= client,
    model_id=llm_bedrock_config.ModelId.LLAMA_3_3_70B,
    model_kwargs=llm_bedrock_config.ModelKwargsLlama(),)