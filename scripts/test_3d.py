"""
3D 模型功能测试脚本

测试图像生成、3D 模型配置和口型同步功能
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


def test_get_voisemes():
    """测试获取音素列表"""
    print(f"\n{'='*50}")
    print("1. 获取音素列表")
    print(f"{'='*50}")

    response = requests.get(f"{BASE_URL}/api/3d/visemes")
    result = response.json()

    print(f"可用音素数量: {result['count']}")
    print("\n前 5 个音素:")
    for viseme in result['visemes'][:5]:
        print(f"  - {viseme['id']}: {viseme['name']} ({viseme['description']})")

    return result


def test_lip_sync():
    """测试口型同步数据生成"""
    print(f"\n{'='*50}")
    print("2. 口型同步数据生成")
    print(f"{'='*50}")

    data = {
        "text": "床前明月光，疑是地上霜。",
        "figure_name": "李白"
    }

    print(f"文本: {data['text']}")

    response = requests.post(f"{BASE_URL}/api/3d/lip-sync", json=data)
    result = response.json()

    print(f"\n生成 {len(result['visemes'])} 个音素")
    print(f"总时长: {result['duration']:.2f} 秒")
    print(f"\n音素序列 (前 10 个):")
    for v in result['visemes'][:10]:
        print(f"  {v['time']:.2f}s: '{v['char']}' -> {v['viseme']}")

    return result


def test_lip_sync_long_text():
    """测试长文本口型同步"""
    print(f"\n{'='*50}")
    print("3. 长文本口型同步")
    print(f"{'='*50}")

    data = {
        "text": "你好，我是李白。我生于唐代，自号青莲居士。我的诗歌豪放飘逸，想象丰富，欢迎大家与我交流诗词！",
        "figure_name": "李白"
    }

    print(f"文本: {data['text']}\n")

    response = requests.post(f"{BASE_URL}/api/3d/lip-sync", json=data)
    result = response.json()

    print(f"生成 {len(result['visemes'])} 个音素")
    print(f"总时长: {result['duration']:.2f} 秒")
    print(f"平均每字符时长: {result['duration']/len(result['visemes']):.3f} 秒")

    return result


def test_get_3d_models():
    """测试获取 3D 模型配置"""
    print(f"\n{'='*50}")
    print("4. 获取 3D 模型配置")
    print(f"{'='*50}")

    response = requests.get(f"{BASE_URL}/api/3d/models")
    result = response.json()

    print(f"共有 {result['count']} 个历史人物配置")
    print(f"\n人物列表:")
    for name, info in result['models'].items():
        has_image = "✅" if info.get('image_url') else "❌"
        print(f"  {has_image} {name}: {info.get('style', 'N/A')}")

    return result


def test_generate_figure_image():
    """测试生成历史人物图像"""
    print(f"\n{'='*50}")
    print("5. 生成历史人物图像")
    print(f"{'='*50}")

    # 测试生成李白图像
    data = {
        "figure_name": "李白",
        "style": "realistic",
        "size": "2K",
        "pose": "portrait",
        "expression": "thoughtful"
    }

    print(f"生成参数: {json.dumps(data, ensure_ascii=False)}")
    print("\n正在生成图像，请稍候...")

    response = requests.post(f"{BASE_URL}/api/3d/generate-image", json=data)

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ 图像生成成功！")
        print(f"图像 URL: {result['image_url']}")
        print(f"风格: {result['style']}")
        print(f"尺寸: {result['size']}")

        # 下载图像
        print("\n正在下载图像...")
        img_response = requests.get(result['image_url'])
        output_file = "/tmp/libai_portrait.png"
        with open(output_file, 'wb') as f:
            f.write(img_response.content)
        print(f"✅ 图像已保存到: {output_file}")

        return result
    else:
        print(f"\n❌ 图像生成失败: {response.text}")
        return None


def test_generate_multiple_images():
    """测试生成多个历史人物图像"""
    print(f"\n{'='*50}")
    print("6. 生成多个历史人物图像")
    print(f"{'='*50}")

    figures = ["爱因斯坦", "孔子"]

    for figure in figures:
        print(f"\n--- {figure} ---")

        data = {
            "figure_name": figure,
            "style": "realistic",
            "size": "2K",
            "pose": "portrait",
            "expression": "neutral"
        }

        response = requests.post(f"{BASE_URL}/api/3d/generate-image", json=data)

        if response.status_code == 200:
            result = response.json()
            print(f"✅ {figure} 图像生成成功")
            print(f"URL: {result['image_url'][:50]}...")
        else:
            print(f"❌ {figure} 图像生成失败")


def test_complete_workflow():
    """测试完整工作流程：图像生成 + 口型同步"""
    print(f"\n{'='*50}")
    print("7. 完整工作流程测试")
    print(f"{'='*50}")

    # 步骤1: 生成对话
    print("\n步骤 1: 发送对话消息给李白")
    chat_data = {
        "message": "请用一首诗来描述月亮",
        "figure_name": "李白"
    }

    chat_response = requests.post(f"{BASE_URL}/api/chat/", json=chat_data)
    if chat_response.status_code != 200:
        print(f"❌ 对话失败")
        return

    chat_result = chat_response.json()
    reply_text = chat_result.get("message", "")
    print(f"李白回复: {reply_text[:100]}...")

    # 步骤2: 生成口型同步数据
    print("\n步骤 2: 生成口型同步数据")
    lip_sync_data = {
        "text": reply_text,
        "figure_name": "李白"
    }

    lip_sync_response = requests.post(f"{BASE_URL}/api/3d/lip-sync", json=lip_sync_data)
    lip_sync_result = lip_sync_response.json()

    print(f"✅ 生成了 {len(lip_sync_result['visemes'])} 个音素")
    print(f"   总时长: {lip_sync_result['duration']:.2f} 秒")

    # 步骤3: 生成语音（如果需要）
    print("\n步骤 3: 生成语音（可选）")
    tts_data = {
        "text": reply_text,
        "figure_name": "李白"
    }

    tts_response = requests.post(f"{BASE_URL}/api/voice/tts", json=tts_data)
    if tts_response.status_code == 200:
        tts_result = tts_response.json()
        print(f"✅ 语音生成成功")
        print(f"   音频 URL: {tts_result['audio_url'][:50]}...")

    print("\n✅ 完整工作流程测试完成！")


def main():
    """运行所有测试"""
    print("开始测试 3D 模型功能...")
    print(f"API 地址: {BASE_URL}")

    try:
        # 测试1: 获取音素列表
        test_get_voisemes()

        # 测试2: 口型同步
        test_lip_sync()

        # 测试3: 长文本口型同步
        test_lip_sync_long_text()

        # 测试4: 获取 3D 模型配置
        test_get_3d_models()

        # 测试5: 生成历史人物图像（跳过，因为需要较长时间）
        print("\n" + "="*50)
        print("注意: 图像生成需要较长时间，跳过")
        print("如需测试，可以单独运行: test_generate_figure_image()")
        print("="*50)

        # test_generate_figure_image()
        # test_generate_multiple_images()

        # 测试6: 完整工作流程
        test_complete_workflow()

        print(f"\n{'='*50}")
        print("✅ 所有 3D 功能测试完成！")
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
