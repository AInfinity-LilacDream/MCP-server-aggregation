from baidusearch.baidusearch import search
import redis
from fastmcp import FastMCP
import json

mcp = FastMCP("baidu search mcp")

sessions = {}

# 使用 decode_responses=True 自动解码
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

try:
    r.ping()
except redis.ConnectionError:
    raise RuntimeError("无法连接到 Redis 服务器，请确保 Redis 正在运行。")

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

    value = r.get(query)
    if value is not None:
        return json.loads(value)

    results = search(query, num_results)
    r.set(query, json.dumps(results))

    return results

@mcp.tool()
def cache_clear():
    """
    Thoroughly clear the cache. This will clear all the data stored in cache irreversibly.
    """
    r.flushall()
    return "Success"

if __name__ == "__main__":
    mcp.run(transport="streamable-http",
            host="localhost",
            port=9000,
            path="/mcp")