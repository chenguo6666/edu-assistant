"""聊天路由：WebSocket 实时通信"""
import json
import traceback
from datetime import datetime
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models.conversation import Conversation, Message
from services.auth_service import decode_token
from agents.edu_agent import create_edu_agent
from agents.admission_agent import create_admission_agent
from agents.callbacks import WebSocketCallbackHandler

router = APIRouter(prefix="/api/chat", tags=["聊天"])


def _get_user_profile(user: User) -> dict:
    """从用户模型中提取画像信息"""
    subjects = None
    if user.subjects:
        try:
            subjects = json.loads(user.subjects)
        except json.JSONDecodeError:
            pass
    return {
        "grade": user.grade,
        "major": user.major,
        "subjects": subjects,
        "gpa": user.gpa,
    }


def _get_chat_history(db: Session, conversation_id: int, limit: int = 20) -> list:
    """获取对话历史，转换为 LangChain 消息格式"""
    from langchain_core.messages import HumanMessage, AIMessage

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    messages.reverse()

    chat_history = []
    for msg in messages:
        if msg.role == "user":
            chat_history.append(HumanMessage(content=msg.content))
        elif msg.role == "assistant":
            chat_history.append(AIMessage(content=msg.content))
    return chat_history


@router.websocket("/ws/{conversation_id}")
async def websocket_chat(websocket: WebSocket, conversation_id: int):
    """WebSocket 聊天端点"""
    # 从 query 参数获取 token 并验证
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001, reason="缺少认证令牌")
        return

    user_id = decode_token(token)
    if user_id is None:
        await websocket.close(code=4001, reason="无效的认证令牌")
        return

    await websocket.accept()

    db = SessionLocal()
    try:
        # 验证对话归属
        conv = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
            .first()
        )
        if not conv:
            await websocket.send_json({"type": "error", "content": "对话不存在"})
            await websocket.close()
            return

        user = db.query(User).filter(User.id == user_id).first()
        user_profile = _get_user_profile(user) if user else None

        while True:
            # 接收用户消息
            raw = await websocket.receive_text()
            data = json.loads(raw)
            user_input = data.get("content", "").strip()

            if not user_input:
                continue

            # 保存用户消息
            user_msg = Message(
                conversation_id=conversation_id,
                role="user",
                content=user_input,
            )
            db.add(user_msg)
            db.commit()

            # 通知前端开始思考
            await websocket.send_json({"type": "thinking_start", "content": "正在分析任务..."})

            # 创建 Agent 和 Callback
            callback = WebSocketCallbackHandler(websocket)

            # 根据对话模式选择 Agent
            if conv.mode == "edu":
                agent = create_edu_agent(user_id=user_id, user_profile=user_profile)
            else:
                agent = create_admission_agent(user_profile=user_profile)

            # 获取对话历史
            chat_history = _get_chat_history(db, conversation_id)

            # 执行 Agent
            try:
                result = await agent.arun(
                    user_input=user_input,
                    chat_history=chat_history,
                    callbacks=[callback],
                )

                output = result.get("output", "抱歉，我无法处理这个请求。")

                # 序列化中间步骤
                steps_data = []
                for step in result.get("intermediate_steps", []):
                    action, observation = step
                    steps_data.append({
                        "tool": action.tool,
                        "input": str(action.tool_input),
                        "output": str(observation)[:500],
                    })

                # 保存 AI 回复
                ai_msg = Message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=output,
                    agent_steps=json.dumps(steps_data, ensure_ascii=False) if steps_data else None,
                )
                db.add(ai_msg)

                # 更新对话标题（首条消息时）
                msg_count = db.query(Message).filter(
                    Message.conversation_id == conversation_id
                ).count()
                if msg_count <= 2:
                    conv.title = user_input[:30] + ("..." if len(user_input) > 30 else "")

                conv.updated_at = datetime.utcnow()
                db.commit()

                # 发送完成信号
                await websocket.send_json({
                    "type": "done",
                    "message_id": ai_msg.id,
                    "content": output,
                    "agent_steps": steps_data,
                })

            except Exception as e:
                traceback.print_exc()
                await websocket.send_json({
                    "type": "error",
                    "content": f"处理失败: {str(e)}",
                })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        traceback.print_exc()
    finally:
        db.close()
