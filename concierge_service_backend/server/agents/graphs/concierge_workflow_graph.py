from langgraph.graph import StateGraph, END
from typing import Any, List
from server.agents.graphs.nodes import intent_categorizer, entities_finder, web_searcher
from server.agents.tools.web_search_tool import duckduckgo_search
from server.agents.states import concierge_workflow_state
from server.config.llm_registry import LLM_MAPPER
from server.utils.tool_str_to_func import tool_str_func_mapping
from server.utils.add_dependencies_to_node import add_dependencies_to_node
from server.prompts import entities_finder_prompts, intent_categorizer_prompts
    

def is_intent_other_node(state: dict) -> bool:
  is_intent_other = state['intent_category'] == 'other'
  return is_intent_other

class Graph:
    def __init__(self, agent_state: concierge_workflow_state.AgentState, tools: List[Any] = [duckduckgo_search]):
        self.agent_state = agent_state
        self.tools = tool_str_func_mapping(tools) if tools else {}
        self.graph = StateGraph(self.agent_state)
        
        self.intent_categorizer_node_with_dependencies = add_dependencies_to_node(
            intent_categorizer.intent_categorizer,
            llm=LLM_MAPPER.get("bedrock_claude_3_7_sonnet"),
            system_prompt=intent_categorizer_prompts.system_prompt,
            human_prompt=intent_categorizer_prompts.human_prompt)
            
        self.entities_finder_node_with_dependencies = add_dependencies_to_node(
            entities_finder.entities_finder,
            llm = LLM_MAPPER.get("bedrock_claude_3_7_sonnet"),
            system_prompt = entities_finder_prompts.system_prompt,
            human_prompt = entities_finder_prompts.human_prompt)
        
        self.web_searcher_node_with_dependencies = add_dependencies_to_node(
            web_searcher.web_searcher,
            tools = self.tools,)
        
        self.graph.add_node("intent_categorizer",self.intent_categorizer_node_with_dependencies )
        
        self.graph.add_node("entities_finder", self.entities_finder_node_with_dependencies)
        
        self.graph.add_node("web_searcher", self.web_searcher_node_with_dependencies) 

        self.graph.set_entry_point("intent_categorizer")
        
        self.graph.add_conditional_edges("intent_categorizer", is_intent_other_node, {True: "web_searcher", False:"entities_finder"})

        self.graph.add_edge("entities_finder", END)
        
        self.graph.add_edge("web_searcher", END)

        self.runnable = self.graph.compile()
    
    async def invoke(self, state: Any) -> Any:
        try:
            return await self.runnable.ainvoke(state)
        except KeyError as e:
            raise ValueError(f"Missing required key in state: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during graph execution: {e}")
