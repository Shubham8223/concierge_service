from langchain_community.tools import DuckDuckGoSearchResults
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from typing import Annotated

class DuckDuckGoSearchInput(BaseModel):
    query: Annotated[str, Field(description="The search query string")]
    max_results: Annotated[
        int, Field(description="Maximum number of results to return", ge=1, le=10)
    ] = 5

    def process_response(self, results: list) -> str:
        if not results:
            return "No results found."

        formatted_results = []
        for item in results[:self.max_results]:
            title = item.get("title", "No title")
            snippet = item.get("snippet", "No snippet available")
            link = item.get("link", "No URL available")
            formatted_results.append(f"Title: {title}\nSnippet: {snippet}\nURL: {link}\n")

        return "\n".join(formatted_results)

@tool("duckduckgo_search")
def duckduckgo_search(search_input: DuckDuckGoSearchInput) -> str:
    """This tool performs a search query using DuckDuckGo to retrieve information related to the user's query.
    It accepts search parameters such as the query string and the maximum number of results to return.

    Args:
    - search_input: A structured input containing the search query string and maximum results to return.

    Returns:
    - A formatted string with the titles, snippets, and URLs of the search results, or a message indicating no results were found.
    """
    search = DuckDuckGoSearchResults(output_format="list",max_results=search_input.max_results)
    try:
        results = search.invoke(search_input.query)
        return search_input.process_response(results)
    except Exception as e:
        return f"An error occurred while performing the search: {str(e)}"