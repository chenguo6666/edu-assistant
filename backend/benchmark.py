"""
性能基准测试：逐层测量 LLM 调用、工具执行、完整 Agent 的耗时
运行方式：cd backend && python benchmark.py
"""
import asyncio
import time
import sys
import os

# 确保能 import 项目模块
sys.path.insert(0, os.path.dirname(__file__))

from langchain_openai import ChatOpenAI
from config import settings

# ─── 工具函数 ────────────────────────────────────────────────

def hline(title=""):
    w = 60
    if title:
        pad = (w - len(title) - 2) // 2
        print(f"\n{'─' * pad} {title} {'─' * pad}")
    else:
        print("─" * w)

def t(label, start):
    elapsed = time.perf_counter() - start
    print(f"  ✓ {label:<38} {elapsed:.2f}s")
    return elapsed

# ─── 原始 LLM 调用测试 ───────────────────────────────────────

async def bench_llm_raw():
    hline("1. 原始 LLM 调用（无 Agent 开销）")

    llm_397 = ChatOpenAI(
        model=settings.SILICONFLOW_MODEL,
        openai_api_key=settings.SILICONFLOW_API_KEY,
        openai_api_base=settings.SILICONFLOW_BASE_URL,
        temperature=0.7, streaming=False, max_tokens=200,
    )
    llm_122 = ChatOpenAI(
        model=settings.SILICONFLOW_MODEL_LITE,
        openai_api_key=settings.SILICONFLOW_API_KEY,
        openai_api_base=settings.SILICONFLOW_BASE_URL,
        temperature=0.7, streaming=False, max_tokens=200,
    )

    prompt_short = "你好，请用一句话介绍你自己。"
    prompt_long  = "请列出小学六年级数学的主要知识点，每点用一句话概括，共10点。"

    print(f"  模型-主力: {settings.SILICONFLOW_MODEL}")
    print(f"  模型-轻量: {settings.SILICONFLOW_MODEL_LITE}")

    # 397B 短问题
    s = time.perf_counter()
    r = await llm_397.ainvoke(prompt_short)
    t1 = t("397B · 短问题（~10 tokens 输出）", s)

    # 397B 长问题
    s = time.perf_counter()
    r = await llm_397.ainvoke(prompt_long)
    t2 = t("397B · 长问题（~200 tokens 输出）", s)

    # 122B 短问题
    s = time.perf_counter()
    r = await llm_122.ainvoke(prompt_short)
    t3 = t("122B · 短问题（~10 tokens 输出）", s)

    # 122B 长问题
    s = time.perf_counter()
    r = await llm_122.ainvoke(prompt_long)
    t4 = t("122B · 长问题（~200 tokens 输出）", s)

    # 397B 第一次 vs 第二次（测试连接复用）
    s = time.perf_counter()
    r = await llm_397.ainvoke(prompt_short)
    t5 = t("397B · 短问题（第 2 次，测连接复用）", s)

    return {"397B_short": t1, "397B_long": t2, "122B_short": t3, "122B_long": t4, "397B_short2": t5}

# ─── 工具内部 LLM 调用测试 ───────────────────────────────────

async def bench_tools():
    hline("2. 工具执行（每个工具单独计时）")

    sample_text = """
    小学六年级数学第一章：分数与小数
    本章主要介绍分数的基本性质、约分、通分、分数加减法、分数乘除法。
    分数的基本性质：分子分母同乘或同除以一个不为零的数，分数的值不变。
    约分：找分子分母的最大公因数，然后同除以该数。
    通分：找分母的最小公倍数作为公分母。
    """ * 3  # 约 400 字

    from agents.tools.summarize import summarize
    from agents.tools.knowledge_extractor import extract_knowledge
    from agents.tools.quiz_generator import generate_quiz
    from agents.tools.study_plan import generate_study_plan

    results = {}

    s = time.perf_counter()
    summarize.invoke({"text": sample_text})
    results["summarize"] = t("summarize（总结）", s)

    s = time.perf_counter()
    extract_knowledge.invoke({"text": sample_text})
    results["extract_knowledge"] = t("extract_knowledge（知识点提取）", s)

    s = time.perf_counter()
    generate_quiz.invoke({"text": sample_text, "count": 3})
    results["generate_quiz_3"] = t("generate_quiz（3 道题）", s)

    s = time.perf_counter()
    generate_study_plan.invoke({"subject": "小学六年级数学", "duration": "1周"})
    results["study_plan"] = t("generate_study_plan（1周计划）", s)

    return results

# ─── Agent 完整链路测试 ──────────────────────────────────────

async def bench_agent_simple():
    hline("3. Agent 完整链路（问题1：简单打招呼）")
    from agents.edu_agent import create_edu_agent

    agent = create_edu_agent()

    s = time.perf_counter()
    result = await agent.arun(user_input="你好")
    elapsed = t("Agent · '你好'（预期 0 工具调用）", s)

    steps = result.get("intermediate_steps", [])
    print(f"  → 实际工具调用数: {len(steps)}")
    print(f"  → 回复前 50 字: {result.get('output','')[:50]}")
    return elapsed


async def bench_agent_tools():
    hline("4. Agent 完整链路（问题2：搜索+制定计划）")
    from agents.edu_agent import create_edu_agent

    agent = create_edu_agent()

    s_total = time.perf_counter()
    result = await agent.arun(
        user_input="帮我上网查询小学六年级数学主要知识点，制定学习计划"
    )
    elapsed = t("Agent · 搜索+计划（预期 2 工具调用）", s_total)

    steps = result.get("intermediate_steps", [])
    print(f"  → 实际工具调用数: {len(steps)}")
    for i, (action, obs) in enumerate(steps):
        print(f"  → 步骤 {i+1}: {action.tool}")
    return elapsed


async def bench_agent_multi():
    hline("5. Agent 完整链路（问题3：RAG+总结+提取+出题）")
    from agents.edu_agent import create_edu_agent

    agent = create_edu_agent(user_id=1)

    sample_article = """
    《草船借箭》
    周瑜嫉妒诸葛亮的才能，想借机除掉他。他让诸葛亮在三天内造好十万支箭。
    诸葛亮不慌不忙，向鲁肃借了二十条船、六百名士兵和大量草把子。
    第三天四更时分，诸葛亮秘密请鲁肃上船，趁着大雾接近曹操的水寨。
    曹军见船来，以为是敌袭，万箭齐发。草把子上很快插满了箭。
    天亮后，二十条船共得了十余万支箭。诸葛亮成功完成任务，周瑜自叹不如。
    这个故事体现了诸葛亮的神机妙算和对天文地理的熟练掌握。
    """ * 5  # 约 500 字

    s_total = time.perf_counter()
    result = await agent.arun(
        user_input=f"请总结以下课文，提取核心知识点，生成3道选择题：\n\n{sample_article}"
    )
    elapsed = t("Agent · 总结+知识点+出题（预期 3 工具调用）", s_total)

    steps = result.get("intermediate_steps", [])
    print(f"  → 实际工具调用数: {len(steps)}")
    for i, (action, obs) in enumerate(steps):
        print(f"  → 步骤 {i+1}: {action.tool}")
    return elapsed

# ─── 主入口 ─────────────────────────────────────────────────

async def main():
    print("\n" + "═" * 60)
    print("  EduAssistant 性能基准测试")
    print("═" * 60)
    print(f"  API Base : {settings.SILICONFLOW_BASE_URL}")
    print(f"  主力模型 : {settings.SILICONFLOW_MODEL}")
    print(f"  轻量模型 : {settings.SILICONFLOW_MODEL_LITE}")

    try:
        llm_results  = await bench_llm_raw()
    except Exception as e:
        print(f"  [跳过] LLM 原始测试失败: {e}")
        llm_results = {}

    try:
        tool_results = await bench_tools()
    except Exception as e:
        print(f"  [跳过] 工具测试失败: {e}")
        tool_results = {}

    try:
        t_simple = await bench_agent_simple()
    except Exception as e:
        print(f"  [跳过] Agent 简单测试失败: {e}")
        t_simple = None

    try:
        t_tools = await bench_agent_tools()
    except Exception as e:
        print(f"  [跳过] Agent 工具链测试失败: {e}")
        t_tools = None

    try:
        t_multi = await bench_agent_multi()
    except Exception as e:
        print(f"  [跳过] Agent 多工具测试失败: {e}")
        t_multi = None

    # ── 汇总 ──
    hline("汇总")
    if llm_results:
        print("\n  LLM 原始延迟（不含 Agent 开销）:")
        print(f"    397B 短 → {llm_results.get('397B_short', '?'):.2f}s   长 → {llm_results.get('397B_long', '?'):.2f}s")
        print(f"    122B 短 → {llm_results.get('122B_short', '?'):.2f}s   长 → {llm_results.get('122B_long', '?'):.2f}s")
        print(f"    397B 连接复用 → {llm_results.get('397B_short2', '?'):.2f}s")

    if tool_results:
        print("\n  工具执行耗时（已含内部 LLM 调用）:")
        for name, val in tool_results.items():
            print(f"    {name:<30} {val:.2f}s")

    print("\n  完整 Agent 耗时（含所有 LLM 调用 + LangChain 开销）:")
    if t_simple is not None: print(f"    问题1 (无工具)    {t_simple:.2f}s")
    if t_tools  is not None: print(f"    问题2 (搜索+计划) {t_tools:.2f}s")
    if t_multi  is not None: print(f"    问题3 (3工具链)   {t_multi:.2f}s")

    if t_tools and tool_results:
        agent_overhead = t_tools - tool_results.get("study_plan", 0)
        print(f"\n  推断 Agent 推理开销 (问题2 - study_plan工具): ~{agent_overhead:.2f}s")

    hline()
    print("  测试完成。\n")


if __name__ == "__main__":
    asyncio.run(main())
