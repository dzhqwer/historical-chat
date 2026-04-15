"""
历史人物对话 API 测试脚本

测试所有 REST API 接口
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def print_response(title, response):
    """打印响应结果"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"状态码: {response.status_code}")
    print(f"响应内容:")
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))


def test_health():
    """测试健康检查接口"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("1. 健康检查", response)


def test_get_figures():
    """测试获取历史人物列表"""
    response = requests.get(f"{BASE_URL}/api/figures/")
    print_response("2. 获取历史人物列表", response)
    return response.json()


def test_get_figure_detail():
    """测试获取历史人物详情"""
    response = requests.get(f"{BASE_URL}/api/figures/detail/李白")
    print_response("3. 获取李白详细信息", response)


def test_chat():
    """测试对话接口"""
    data = {
        "message": "你好，我是谁？",
        "figure_name": "李白",
        "session_id": "test-session-001"
    }
    response = requests.post(f"{BASE_URL}/api/chat/", json=data)
    print_response("4. 与李白对话", response)


def test_chat_history():
    """测试获取对话历史"""
    response = requests.get(f"{BASE_URL}/api/chat/history/test-session-001")
    print_response("5. 获取对话历史", response)


def main():
    """运行所有测试"""
    print("开始测试历史人物对话 API...")
    print(f"API 地址: {BASE_URL}")
    print(f"API 文档: {BASE_URL}/docs")

    try:
        # 测试健康检查
        test_health()

        # 测试获取人物列表
        figures = test_get_figures()

        # 测试获取人物详情
        test_get_figure_detail()

        # 测试对话
        test_chat()

        # 测试获取对话历史
        test_chat_history()

        print(f"\n{'='*50}")
        print("✅ 所有测试完成！")
        print(f"{'='*50}")

    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到服务器")
        print("请确保服务器正在运行: python scripts/start_api.sh")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")


if __name__ == "__main__":
    main()
