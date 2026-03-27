"""联网搜索工具：通过 SerpAPI 实时搜索互联网信息"""
from langchain_core.tools import tool
from config import settings


@tool
def web_search(query: str) -> str:
    """搜索互联网获取最新信息。当需要查询实时数据、最新政策、新闻等信息时使用此工具。

    Args:
        query: 搜索关键词
    """
    try:
        from serpapi import GoogleSearch
        params = {
            "q": query,
            "api_key": settings.SERPAPI_API_KEY,
            "engine": "google",
            "num": 5,
            "hl": "zh-cn",
            "gl": "cn",
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        # 提取搜索结果摘要
        snippets = []
        for item in results.get("organic_results", [])[:5]:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            snippets.append(f"**{title}**\n{snippet}\n来源: {link}")

        if not snippets:
            return "未找到相关搜索结果。"

        return "\n\n".join(snippets)
    except Exception as e:
        return f"搜索失败: {str(e)}"
