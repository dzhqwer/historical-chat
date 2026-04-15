"""
WebSocket 实时对话测试脚本
"""
import asyncio
import websockets
import json


async def test_websocket():
    """测试 WebSocket 实时流式对话"""
    uri = "ws://localhost:8000/api/ws/chat"

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket 连接成功")

            # 接收连接确认消息
            welcome_msg = await websocket.recv()
            print(f"服务器消息: {json.loads(welcome_msg)}\n")

            # 发送对话消息
            message = {
                "type": "message",
                "content": "请用简单的话介绍一下你自己",
                "figure_name": "孔子"
            }

            print(f"发送消息: {json.dumps(message, ensure_ascii=False)}\n")
            await websocket.send(json.dumps(message))

            # 接收流式响应
            print("开始接收流式响应:")
            print("=" * 60)

            full_response = ""
            while True:
                response = await websocket.recv()
                data = json.loads(response)

                if data.get("type") == "chunk":
                    content = data.get("content", "")
                    print(content, end="", flush=True)
                    full_response += content
                elif data.get("type") == "done":
                    print("\n")
                    print("=" * 60)
                    print(f"✅ 对话完成，会话ID: {data.get('session_id')}")
                    print(f"完整回复长度: {len(full_response)} 字符")
                    break
                elif data.get("type") == "error":
                    print(f"\n❌ 错误: {data.get('message')}")
                    break

    except websockets.exceptions.ConnectionRefused:
        print("❌ 无法连接到 WebSocket 服务器")
        print("请确保服务器正在运行: python scripts/start_api.sh")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    print("开始测试 WebSocket 实时对话...")
    print("WebSocket 地址: ws://localhost:8000/api/ws/chat\n")

    # 检查是否安装了 websockets
    try:
        import websockets
    except ImportError:
        print("❌ 未安装 websockets 库")
        print("请运行: uv pip install websockets")
        exit(1)

    asyncio.run(test_websocket())
