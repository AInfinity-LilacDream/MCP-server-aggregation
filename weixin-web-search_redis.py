from miku_ai import get_wexin_article
from pydantic import BaseModel
from typing import List
import uvicorn
import redis
import json

from fastmcp import FastMCP

# 创建FastMCP应用
mcp = FastMCP("微信文章搜索MCP服务")

# 使用 decode_responses=True 自动解码
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 定义数据模型
class ArticleResponse(BaseModel):
    title: str
    url: str
    source: str
    date: str

class ArticleSearchRequest(BaseModel):
    query: str
    top_num: int = 5  # 添加可选参数，默认为5条

class ArticleSearchResponse(BaseModel):
    articles: List[ArticleResponse]
    total_count: int

# 文章搜索端点
@mcp.tool()
async def search_articles(query: str, top_num: int = 5):
    """搜索微信文章"""

    value = r.get(query.strip())
    if value is not None:
        data = json.loads(value)
        output_articles = [ArticleResponse.model_validate(item) for item in data]
    else:
        articles = await get_wexin_article(query.strip(), top_num)

        output_articles = [
            ArticleResponse(
                title=article.get('title', ''),
                url=article.get('url', ''),
                source=article.get('source', ''),
                date=article.get('date', '')
            ) for article in articles
        ]

        json_str = json.dumps([a.model_dump() for a in output_articles])

        r.set(query.strip(), json_str)

    return ArticleSearchResponse(
        articles=output_articles,
        total_count=len(output_articles)
    )

if __name__ == "__main__":
    mcp.run(transport="streamable-http",
            host="localhost",
            port=9001,
            path="/mcp")
