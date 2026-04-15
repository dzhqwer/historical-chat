"""
语音功能测试脚本

测试语音识别（ASR）和语音合成（TTS）接口
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
    try:
        print(f"响应内容:")
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except:
        print(f"响应内容: {response.text}")


def test_get_voices():
    """测试获取可用音色列表"""
    print(f"\n{'='*50}")
    print("1. 获取可用音色列表")
    print(f"{'='*50}")

    response = requests.get(f"{BASE_URL}/api/voice/voices")
    print_response("", response)
    return response.json()


def test_tts():
    """测试文字转语音（TTS）"""
    print(f"\n{'='*50}")
    print("2. 文字转语音（TTS）- 李白")
    print(f"{'='*50}")

    data = {
        "text": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
        "figure_name": "李白"
    }

    print(f"发送数据: {json.dumps(data, ensure_ascii=False)}")

    response = requests.post(f"{BASE_URL}/api/voice/tts", json=data)
    result = response.json()

    print(f"\n音频 URL: {result.get('audio_url')}")
    print(f"音频大小: {result.get('audio_size')} 字节")
    print(f"预估时长: {result.get('duration', 0):.2f} 秒")
    print(f"使用音色: {result.get('speaker')}")

    # 下载音频文件
    audio_url = result.get('audio_url')
    if audio_url:
        print("\n正在下载音频文件...")
        audio_response = requests.get(audio_url)
        output_file = "/tmp/libai_test.mp3"
        with open(output_file, 'wb') as f:
            f.write(audio_response.content)
        print(f"✅ 音频已保存到: {output_file}")

    return result


def test_tts_custom_voice():
    """测试使用自定义音色的文字转语音"""
    print(f"\n{'='*50}")
    print("3. 文字转语音（TTS）- 自定义音色")
    print(f"{'='*50}")

    data = {
        "text": "你好，我是爱因斯坦。E equals m c squared.",
        "speaker": "zh_male_m191_uranus_bigtts",
        "speech_rate": 10,
        "sample_rate": 48000
    }

    print(f"发送数据: {json.dumps(data, ensure_ascii=False)}")

    response = requests.post(f"{BASE_URL}/api/voice/tts", json=data)
    result = response.json()

    print(f"\n音频 URL: {result.get('audio_url')}")
    print(f"音频大小: {result.get('audio_size')} 字节")
    print(f"使用音色: {result.get('speaker')}")

    # 下载音频文件
    audio_url = result.get('audio_url')
    if audio_url:
        print("\n正在下载音频文件...")
        audio_response = requests.get(audio_url)
        output_file = "/tmp/einstein_test.mp3"
        with open(output_file, 'wb') as f:
            f.write(audio_response.content)
        print(f"✅ 音频已保存到: {output_file}")

    return result


def test_tts_all_figures():
    """测试所有历史人物的语音合成"""
    print(f"\n{'='*50}")
    print("4. 测试所有历史人物的语音合成")
    print(f"{'='*50}")

    figures = ["李白", "爱因斯坦", "孔子", "秦始皇", "莎士比亚", "苏格拉底"]

    for figure in figures:
        print(f"\n--- {figure} ---")
        data = {
            "text": f"我是{figure}，很高兴认识你。",
            "figure_name": figure
        }

        response = requests.post(f"{BASE_URL}/api/voice/tts", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {figure}: {result.get('speaker')}")
        else:
            print(f"❌ {figure}: {response.status_code}")


def test_tts_with_chat():
    """测试对话 + 语音合成完整流程"""
    print(f"\n{'='*50}")
    print("5. 对话 + 语音合成完整流程")
    print(f"{'='*50}")

    # 步骤1: 发送对话消息
    print("\n步骤 1: 发送对话消息给孔子")
    chat_data = {
        "message": "用简单的话介绍一下你自己",
        "figure_name": "孔子"
    }

    chat_response = requests.post(f"{BASE_URL}/api/chat/", json=chat_data)
    chat_result = chat_response.json()
    reply_text = chat_result.get("message", "")

    print(f"孔子回复: {reply_text[:100]}...")

    # 步骤2: 将回复转换为语音
    print("\n步骤 2: 将回复转换为语音")
    tts_data = {
        "text": reply_text,
        "figure_name": "孔子"
    }

    tts_response = requests.post(f"{BASE_URL}/api/voice/tts", json=tts_data)
    tts_result = tts_response.json()

    print(f"音频 URL: {tts_result.get('audio_url')}")
    print(f"音频大小: {tts_result.get('audio_size')} 字节")

    # 下载音频
    audio_url = tts_result.get('audio_url')
    if audio_url:
        audio_response = requests.get(audio_url)
        output_file = "/tmp/confucius_full.mp3"
        with open(output_file, 'wb') as f:
            f.write(audio_response.content)
        print(f"✅ 完整对话音频已保存到: {output_file}")


def main():
    """运行所有测试"""
    print("开始测试语音功能...")
    print(f"API 地址: {BASE_URL}")

    try:
        # 测试1: 获取音色列表
        test_get_voices()

        # 测试2: TTS - 李白
        test_tts()

        # 测试3: TTS - 自定义音色
        test_tts_custom_voice()

        # 测试4: 测试所有历史人物
        test_tts_all_figures()

        # 测试5: 对话 + 语音合成完整流程
        test_tts_with_chat()

        print(f"\n{'='*50}")
        print("✅ 所有语音功能测试完成！")
        print(f"{'='*50}")

    except requests.exceptions.ConnectionError:
        print("\n❌ 错误: 无法连接到服务器")
        print("请确保服务器正在运行: python scripts/start_api.sh")
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
