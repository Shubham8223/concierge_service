from server.config.llms import anthropic, meta

LLM_MAPPER = {
    "bedrock_claude_3_7_sonnet": anthropic.bedrock_claude_3_7_sonnet,
    "bedrock_claude_3_5_sonnet": anthropic.bedrock_claude_3_5_sonnet,
    "bedrock_llama_3_3": meta.bedrock_llama_3_3
}