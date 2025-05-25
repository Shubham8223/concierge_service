from langgraph.graph import StateGraph, END
from typing import Any
from server.agents.graphs.nodes import intent_categorizer, entities_finder, web_searcher
from server.agents.states import concierge_workflow_state
from server.config.llm_registry import LLM_MAPPER
    

def is_intent_other_node(state: dict) -> bool:
  is_intent_other = state['intent_category'] == 'other'
  return is_intent_other

class Graph:
    def __init__(self, AgentState: concierge_workflow_state.AgentState):
        self.AgentState = AgentState
        self.graph = StateGraph(self.AgentState)

        self.graph.add_node("intent_categorizer",intent_categorizer.intent_categorizer )
        self.graph.add_node("entities_finder", entities_finder.entities_finder)
        self.graph.add_node("web_searcher", web_searcher.web_searcher) 

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
