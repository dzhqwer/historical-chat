<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>历史人物对话系统</title>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- React -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>

    <!-- Babel for JSX -->
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- Three.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <!-- Socket.io -->
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>

    <!-- Axios -->
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

    <!-- ⭐ 需要修改的地方：API URL ⭐ -->
    <script>
        // 后端 API 地址
        const API_BASE_URL = 'https://historical-chat-kxnh.vercel.app/api';
    </script>

    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        #root {
            min-height: 100vh;
        }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        // 内置的历史人物数据（如果 API 失败，使用这个备用数据）
        const defaultFigures = [
            { id: 1, name: "李白", era: "唐代", description: "唐代著名诗人，字太白，号青莲居士", avatar: "👨‍🎤" },
            { id: 2, name: "孔子", era: "春秋", description: "儒家学派创始人，教育家", avatar: "👴" },
            { id: 3, name: "爱因斯坦", era: "现代", description: "理论物理学家，相对论创立者", avatar: "👨‍🔬" },
            { id: 4, name: "牛顿", era: "近代", description: "物理学家，牛顿力学创立者", avatar: "👨‍🔬" },
            { id: 5, name: "莎士比亚", era: "文艺复兴", description: "英国剧作家，诗人", avatar: "🎭" }
        ];

        function App() {
            const [figures, setFigures] = useState([]);
            const [selectedFigure, setSelectedFigure] = useState(null);
            const [messages, setMessages] = useState([]);
            const [inputText, setInputText] = useState('');
            const [loading, setLoading] = useState(false);
            const [show3D, setShow3D] = useState(true);
            const [apiError, setApiError] = useState(false);
            const messagesEndRef = useRef(null);

            // 加载历史人物列表
            useEffect(() => {
                loadFigures();
            }, []);

            // 自动滚动到底部
            useEffect(() => {
                scrollToBottom();
            }, [messages]);

            const scrollToBottom = () => {
                messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
            };

            const loadFigures = async () => {
                try {
                    setApiError(false);
                    const response = await axios.get(`${API_BASE_URL}/figures`, {
                        timeout: 5000
                    });
                    
                    if (response.data && response.data.figures) {
                        setFigures(response.data.figures);
                    } else {
                        console.warn('API 返回格式不正确，使用内置数据');
                        setFigures(defaultFigures);
                    }
                } catch (error) {
                    console.error('加载历史人物失败:', error);
                    setApiError(true);
                    setFigures(defaultFigures);
                }
            };

            const selectFigure = (figure) => {
                setSelectedFigure(figure);
                setMessages([
                    { role: 'assistant', content: `你好！我是${figure.name}（${figure.era}）。${figure.description}。有什么我可以帮你的吗？` }
                ]);
            };

            const sendMessage = async () => {
                if (!inputText.trim() || !selectedFigure) return;

                const userMessage = inputText.trim();
                setInputText('');
                setLoading(true);

                // 添加用户消息
                setMessages(prev => [...prev, { role: 'user', content: userMessage }]);

                try {
                    const response = await axios.post(`${API_BASE_URL}/chat`, {
                        message: userMessage,
                        figure: selectedFigure.name,
                        history: messages
                    }, {
                        timeout: 10000
                    });

                    // 处理不同的响应格式
                    let assistantMessage = '';
                    if (response.data && response.data.message) {
                        assistantMessage = response.data.message;
                    } else if (response.data && response.data.response) {
                        assistantMessage = response.data.response;
                    } else {
                        assistantMessage = '抱歉，我现在无法回答这个问题。';
                    }
                    
                    setMessages(prev => [...prev, { role: 'assistant', content: assistantMessage }]);
                } catch (error) {
                    console.error('发送消息失败:', error);
                    // 模拟回复
                    const mockResponses = [
                        `这是一个很有趣的问题！作为${selectedFigure.name}，我会从我的角度来回答。`,
                        `关于这个问题，我有这样的想法...`,
                        `在我们的时代，这个问题是这样的...`
                    ];
                    const randomResponse = mockResponses[Math.floor(Math.random() * mockResponses.length)];
                    
                    setMessages(prev => [...prev, { 
                        role: 'assistant', 
                        content: `（模拟回复）${randomResponse}` 
                    }]);
                } finally {
                    setLoading(false);
                }
            };

            const handleKeyPress = (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendMessage();
                }
            };

            return (
                <div className="flex h-screen">
                    {/* 左侧：历史人物选择 */}
                    <div className="w-80 bg-white bg-opacity-10 backdrop-blur-lg p-4 overflow-y-auto">
                        <h2 className="text-2xl font-bold text-white mb-4">历史人物</h2>
                        
                        {apiError && (
                            <div className="mb-4 p-2 bg-red-500 bg-opacity-20 rounded text-white text-sm">
                                ⚠️ API 连接失败，使用内置数据
                            </div>
                        )}
                        
                        {figures.map((figure) => (
                            <div
                                key={figure.id}
                                onClick={() => selectFigure(figure)}
                                className={`p-4 mb-3 rounded-lg cursor-pointer transition-all duration-200 ${
                                    selectedFigure?.id === figure.id
                                        ? 'bg-white bg-opacity-20 shadow-lg'
                                        : 'bg-white bg-opacity-5 hover:bg-opacity-10'
                                }`}
                            >
                                <div className="text-4xl mb-2">{figure.avatar}</div>
                                <h3 className="text-lg font-semibold text-white">{figure.name}</h3>
                                <p className="text-sm text-gray-300">{figure.era}</p>
                            </div>
                        ))}
                    </div>

                    {/* 右侧：对话区域 */}
                    <div className="flex-1 flex flex-col">
                        {/* 顶部：人物信息 */}
                        <div className="bg-white bg-opacity-10 backdrop-blur-lg p-4">
                            {selectedFigure ? (
                                <div className="flex items-center justify-between">
                                    <div>
                                        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                                            <span className="text-4xl">{selectedFigure.avatar}</span>
                                            {selectedFigure.name}
                                        </h1>
                                        <p className="text-gray-300 mt-1">{selectedFigure.description}</p>
                                    </div>
                                    <button
                                        onClick={() => setShow3D(!show3D)}
                                        className="px-4 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-colors"
                                    >
                                        {show3D ? '隐藏 3D' : '显示 3D'}
                                    </button>
                                </div>
                            ) : (
                                <h1 className="text-2xl font-bold text-white">请选择一个历史人物开始对话</h1>
                            )}
                        </div>

                        {/* 3D 模型占位符 */}
                        {show3D && selectedFigure && (
                            <div className="flex-1 bg-black bg-opacity-20 relative flex items-center justify-center">
                                <div className="text-white text-center">
                                    <div className="text-8xl mb-4">{selectedFigure.avatar}</div>
                                    <p className="text-gray-400">3D 模型功能开发中</p>
                                </div>
                            </div>
                        )}

                        {/* 消息区域 */}
                        <div className="flex-1 bg-white bg-opacity-10 backdrop-blur-lg p-4 overflow-y-auto" style={{ maxHeight: show3D ? '300px' : '500px' }}>
                            {messages.map((message, index) => (
                                <div key={index} className={`mb-4 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                                    <div className={`inline-block max-w-xs lg:max-w-md xl:max-w-lg px-4 py-2 rounded-lg ${
                                        message.role === 'user'
                                            ? 'bg-purple-500 text-white'
                                            : 'bg-white bg-opacity-20 text-white'
                                    }`}>
                                        {message.content}
                                    </div>
                                </div>
                            ))}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* 输入区域 */}
                        <div className="bg-white bg-opacity-10 backdrop-blur-lg p-4">
                            <div className="flex gap-2">
                                <textarea
                                    value={inputText}
                                    onChange={(e) => setInputText(e.target.value)}
                                    onKeyPress={handleKeyPress}
                                    placeholder="输入你的消息..."
                                    className="flex-1 bg-white bg-opacity-20 text-white placeholder-gray-300 rounded-lg p-3 resize-none focus:outline-none focus:ring-2 focus:ring-purple-500"
                                    rows="2"
                                    disabled={!selectedFigure || loading}
                                />
                                <button
                                    onClick={sendMessage}
                                    disabled={!selectedFigure || loading}
                                    className="px-6 py-2 bg-purple-500 hover:bg-purple-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                    {loading ? '发送中...' : '发送'}
                                </button>
                            </div>
                            {apiError && (
                                <div className="mt-2 text-sm text-yellow-300">
                                    ⚠️ 注意：后端 API 未正常工作，当前使用模拟数据
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            );
        }

        ReactDOM.render(<App />, document.getElementById('root'));
    </script>
</body>
</html>
