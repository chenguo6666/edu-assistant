"""保研知识库初始化脚本：将预置数据加载到 ChromaDB"""
import os
import sys
import json

# 将 backend 目录加入 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.documents import Document
from rag.vector_store import get_vector_store
from rag.document_loader import load_and_split

ADMISSION_COLLECTION = "admission_knowledge"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))


def load_schools_data(file_path: str) -> list[Document]:
    """将 schools.json 转换为 Document 列表"""
    with open(file_path, encoding="utf-8") as f:
        schools = json.load(f)

    docs = []
    for school in schools:
        # 将每所学校的信息格式化为自然语言文本
        content = f"""学校：{school['school']}
院系：{school['department']}
地点：{school['location']}
层次：{school['level']}
招生项目：{', '.join(school['programs'])}
名额类型：{school['quota_type']}

申请要求：
- 成绩：{school['requirements']['gpa']}
- 英语：{school['requirements']['english']}
- 科研：{school['requirements']['research']}
- 考核：{school['requirements']['other']}

时间安排：
- 报名时间：{school['timeline']['open_time']}
- 考核时间：{school['timeline']['exam_time']}
- 录取时间：{school['timeline']['offer_time']}

备注：{school['notes']}
官网：{school['official_url']}"""

        docs.append(Document(
            page_content=content,
            metadata={"source": "schools", "school": school["school"], "filename": "schools.json"},
        ))
    return docs


def load_timeline_data(file_path: str) -> list[Document]:
    """将 timeline.json 转换为 Document 列表"""
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for phase in data["phases"]:
        content = f"""保研阶段：{phase['phase']}
时间：{phase['time']}
主要任务：
""" + "\n".join(f"- {t}" for t in phase["tasks"])

        docs.append(Document(
            page_content=content,
            metadata={"source": "timeline", "phase": phase["phase"], "filename": "timeline.json"},
        ))

    # 重要注意事项单独作为一个文档
    notes_content = "保研重要注意事项：\n" + "\n".join(f"- {n}" for n in data["important_notes"])
    docs.append(Document(
        page_content=notes_content,
        metadata={"source": "timeline", "phase": "注意事项", "filename": "timeline.json"},
    ))
    return docs


def init_admission_knowledge():
    """初始化保研知识库"""
    print("开始初始化保研知识库...")
    vector_store = get_vector_store(ADMISSION_COLLECTION)

    # 检查是否已初始化（避免重复添加）
    existing = vector_store.get()
    if existing and existing.get("ids") and len(existing["ids"]) > 0:
        print(f"知识库已存在 {len(existing['ids'])} 条记录，跳过初始化")
        return

    all_docs = []

    # 加载院校数据
    schools_file = os.path.join(DATA_DIR, "schools.json")
    if os.path.exists(schools_file):
        school_docs = load_schools_data(schools_file)
        all_docs.extend(school_docs)
        print(f"已加载院校数据：{len(school_docs)} 条")

    # 加载时间线数据
    timeline_file = os.path.join(DATA_DIR, "timeline.json")
    if os.path.exists(timeline_file):
        timeline_docs = load_timeline_data(timeline_file)
        all_docs.extend(timeline_docs)
        print(f"已加载时间线数据：{len(timeline_docs)} 条")

    # 加载经验帖（Markdown 文件）
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".md"):
            filepath = os.path.join(DATA_DIR, filename)
            chunks = load_and_split(filepath, filename)
            all_docs.extend(chunks)
            print(f"已加载经验帖 {filename}：{len(chunks)} 段")

    if all_docs:
        vector_store.add_documents(all_docs)
        print(f"保研知识库初始化完成，共 {len(all_docs)} 条记录")
    else:
        print("未找到数据文件，跳过初始化")


if __name__ == "__main__":
    init_admission_knowledge()
