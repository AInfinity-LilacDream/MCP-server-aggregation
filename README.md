# MCP Server 整合 —— 问问旦挞周会
根据前期调研，整合了五个工具，本仓库中包含三个，其余两个为远程仓库。
# 项目结构：
## - weixin-web-search_redis.py
微信公众号搜索引擎，基于搜狗微信搜索API，支持redis缓存
## - baidu_search_redis.py
百度搜索API，支持redis缓存
## - mcp-python-interpreter/mcp-python-interpreter/server.py
python解释器，支持在对话窗口中运行代码并输出结果

# setup instructions:
首先，克隆本仓库。cd到项目路径。
```
pip install -r requirements.txt
python weixin-web-search_redis.py &
python baidu_search_redis.py &
cd mcp-python-interpreter
cd mcp_python_interpreter
python server.py &
```
依次启动三个Streamable http MCP server。
address:
http://localhost:9000/mcp
http://localhost:9001/mcp
http://localhost:9002/mcp

剩余两个远程启动的MCP Server：
- Firecrawl-MCP:
```
{
  "mcpServers": {
    "mcp-server-firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```
- playwright
```
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": [
        "@playwright/mcp@latest",
        "--caps=pdf"
      ]
    }
  }
}
```
  
