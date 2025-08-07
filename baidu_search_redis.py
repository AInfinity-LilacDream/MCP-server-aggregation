from baidusearch.baidusearch import search
import redis
from fastmcp import FastMCP
import json

mcp = FastMCP("baidu search mcp")

@mcp.tool()
async def baidu_search(query: str, num_results: int):
    """
    Search the web and optionally extract content from search results. This is the most powerful search tool available, and if available you should always default to using this tool for any web search needs.

    **Best for:** Finding specific information across multiple websites, when you don't know which website has the information; when you need the most relevant content for a query.
    **Not recommended for:** When you already know which website to scrape (use scrape); when you need comprehensive coverage of a single website (use map or crawl).
    **Common mistakes:** Using crawl or map for open-ended questions (use search instead).
    **Prompt Example:** 'Find the latest research papers on AI published in 2023.'
    :return: a list of dict contains search results.
    """
    results = search(query, num_results)
    return results

if __name__ == "__main__":
    mcp.run(transport="streamable-http",
            host="localhost",
            port=9000,
            path="/mcp")