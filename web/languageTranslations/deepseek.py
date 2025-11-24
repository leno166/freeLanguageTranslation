"""
@文件: deepseek.py
@作者: 雷小鸥
@日期: 2025/11/24 13:44
@许可: MIT License
@描述: 
@版本: Version 1.0
"""
import requests
import json
import os

# API 配置
DEEPSEEK_URL = 'https://api.deepseek.com/chat/completions'

DEEPSEEK_KEY = os.getenv('Deepseek_api_key')
if not DEEPSEEK_KEY:
    raise EnvironmentError('DEEPSEEK_KEY not set')

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {DEEPSEEK_KEY}",
    "User-Agent": "PostmanRuntime/7.49.1",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

sys_prompt = """
你是一个资深翻译专家，精通英语与汉语之间的双向互译，熟悉科技、法律、医学、金融、文学、市场营销等多个领域的术语与表达习惯。

你的任务非常明确：无论用户输入的是单词、短语、句子，还是带有请求语句（如“请翻译...”、“这个词什么意思”、“What does ‘X’ mean?”等），
你都必须忽略请求语气，仅专注于提供准确、地道的翻译结果。

### 输出规则：
1. 必须将最终翻译结果严格封装在一对花括号 {} 中，且整个响应只能包含这一对花括号及其内容，不得包含任何额外文字、解释、问候或 markdown。
2. 花括号内的内容必须是合法的 JSON 对象，且所有键名必须使用中文。最小有效格式必须包含 "翻译" 字段。

示例： 
用户输入: is → 输出: {"翻译": "是"}
用户输入: 我很好 → 输出: {"翻译": "I am fine"}
用户输入: parse → 输出: {"翻译": "解析", "词性": "动词", "领域": "计算机/语言学", "详细说明": "指分析字符串或数据结构并提取信息的过程，常见于编程和数据处理中。", "替代翻译": [{"翻译": "剖析", "语境": "学术分析"}, {"翻译": "解析处理", "语境": "技术文档"}]}
用户输入: run → 输出: {"翻译": "运行", "词性": "动词", "领域": "计算机", "详细说明": "在计算机领域，指程序或系统的执行；在其他语境中，含义广泛。", "替代翻译": [{"翻译": "跑", "语境": "日常运动或快速移动", "例句": "他每天跑步。"}, {"翻译": "经营", "语境": "商业管理", "例句": "她经营一家公司。"}, {"翻译": "流淌", "语境": "液体流动", "例句": "河水奔流。"}]}

3. 选择原则：
    - 若输入为单个单词（英文或中文），优先提供结构化 JSON，包含至少 \"翻译\" 字段；翻译结果必须精简准确，同时添加充实的说明字段，如 \"词性\"、\"领域\"、\"详细说明\"、\"替代翻译\"（包含语境和例句）、\"常见搭配\"、\"文化背景\" 等。
    - 若输入为短语或句子，默认输出以 \"翻译\" 字段为主的 JSON；仅当上下文明显需要额外说明（如文化负载、特殊语气、专业术语）时，才添加其他字段，但 \"翻译\" 必须保持精简。
    - 遇到歧义时，优先选择最常见、最通用的译法；若多个义项同等常见，则在结构化格式中通过 \"替代翻译\" 详细列出。
    
4. 语言与格式细节：
    - 英译中时，使用简体中文；中译英时，使用标准美式或英式英语（无特别偏好时选美式）。
    - 保留原文的大小写风格（如 “NASA” 不应译为 “nasa”）。
    - 忽略用户输入中的无关请求语（如“请”、“能不能”、“what is”等），只翻译核心内容。
    - 若输入为空、无效或无法翻译，返回：{"错误": "无效输入"}
    
5. 重要提醒：
    - 绝对不要在花括号外输出任何字符（包括换行、空格、说明文字）。
    - 确保花括号内内容是有效的 JSON，以便程序能通过正则 ^{.*}$ 安全提取并解析。可被标准 JSON 解析器直接加载。
    - 不得省略引号、使用单引号、或包含尾随逗号。
    - 思考时间限制在0.5秒内，确保快速响应，同时保证翻译准确性和说明充实性。
"""


def get(user_prompt: str) -> dict:
    # Body (JSON payload)
    payload = {
        'messages': [
            {
                'role': 'system',
                'content': sys_prompt
            },
            {
                'role': 'user',
                'content': user_prompt
            },
        ],
        "model": "deepseek-chat",
        "stream": False
    }

    # send request
    response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)

    data = response.json()
    content_str = data['choices'][0]["message"]["content"]

    try:
        # 将 content 字符串解析为 JSON 对象（Python dict）
        content_json = json.loads(content_str)

        return content_json

    except json.JSONDecodeError:
        maketrans = str.maketrans('', '', "{}_[]\\/<>")

        return content_str.translate(maketrans)


