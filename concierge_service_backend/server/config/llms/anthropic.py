from server.config.bedrock import get_bedrock_client
from server.config.langchain.config import get_bedrock_model 
from server.config.langchain import llm_bedrock_config


client = get_bedrock_client()

bedrock_claude_3_5_sonnet = get_bedrock_model(
    client=client,
    model_id=llm_bedrock_config.ModelId.CLAUDE_3_5_SONNET,
    model_kwargs=llm_bedrock_config.ModelKwargsClaude())

bedrock_claude_3_7_sonnet = get_bedrock_model(
    client=client,
    model_id=llm_bedrock_config.ModelId.CLAUDE_3_7_SONNET,
    model_kwargs=llm_bedrock_config.ModelKwargsClaude())