from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Annotated

class DuckDuckGoSearchInput(BaseModel):
    query: Annotated[str, Field(description="The search query string")]
    max_results: Annotated[
        int, Field(description="Maximum number of results to return", ge=1, le=10)
    ] = 5

    def process_response(self, results: list) -> list[dict]:
        if not results:
            return []

        processed_results = []
        for item in results[:self.max_results]:
            processed_results.append({
                "title": item.get("title", "No title"),
                "snippet": item.get("snippet", "No snippet available"),
                "url": item.get("link", "No URL available")
            })

        return processed_results

@tool("duckduckgo_search")
def duckduckgo_search(search_input: DuckDuckGoSearchInput) -> str:
    """This tool performs a search query using DuckDuckGo to retrieve information related to the user's query.
    It accepts search parameters such as the query string and the maximum number of results to return.

    Args:
    - search_input: A structured input containing the search query string and maximum results to return.

    Returns:
    - list of dict: A list containing up to max_results dictionaries
           - 'title': Title of the search result or 'No title' if missing.
           - 'snippet': Snippet or summary of the result or 'No snippet available' if missing.
           - 'url': URL of the result or 'No URL available' if missing.
    """
    search = DuckDuckGoSearchResults(output_format="list",max_results=search_input.max_results)
    try:
        results = search.invoke(search_input.query)
        return search_input.process_response(results)
    except Exception as e:
        return f"An error occurred while performing the search: {str(e)}"