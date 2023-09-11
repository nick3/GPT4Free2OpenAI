# save this as app.py
import random
import string
import time
import json
from flask import (
    Flask,
    Response,
    request
)
import g4f
from g4f.Provider import (
    Acytoo,
    Aichat,
    Ails,
    Bard,
    Bing,
    ChatgptAi,
    ChatgptLogin,
    DeepAi,
    EasyChat,
    Equing,
    GetGpt,
    H2o,
    HuggingChat,
    Opchatgpts,
    OpenAssistant,
    OpenaiChat,
    Raycast,
    Theb,
    Vercel,
    Wewordle,
    Wuguokai,
    You,
    Yqcloud
)

app = Flask(__name__)

@app.route("/ping")
def hello():
    return "pong"


def streaming(model, messages, provider):
    response = g4f.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=True,
        provider=provider,
    )

    completion_id = "".join(random.choices(string.ascii_letters + string.digits, k=28))
    completion_timestamp = int(time.time())
    try:
        for chunk in response:
            completion_data = {
                "id": f"chatcmpl-{completion_id}",
                "object": "chat.completion.chunk",
                "created": completion_timestamp,
                "model": model,
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": chunk,
                        },
                        "finish_reason": None,
                    }
                ],
            }
            # 将 completion_data 转为字符串后返回
            content = json.dumps(completion_data, separators=(",", ":"))
            yield f"data: {content}\n\n"
        yield "data: [DONE]\n\n"
    except GeneratorExit:
        # 处理 GeneratorExit 异常的逻辑
        pass

@app.route("/<string:site>/v1/chat/completions", methods=['OPTIONS', 'POST'])
def chat_completions(site):
    # 通过用户请求地址中的 site 变量，得到对应的 provider
    if site == "chatgptai":
        provider = ChatgptAi
    elif site == "ails":
        provider = Ails
    elif site == "aichat":
        provider = Aichat
    elif site == "acytoo":
        provider = Acytoo
    elif site == "bard":
        provider = Bard
    elif site == "easychat":
        provider = EasyChat
    elif site == "equing":
        provider = Equing
    elif site == "bing":
        provider = Bing
    elif site == "chatgptlogin":
        provider = ChatgptLogin
    elif site == "deepai":
        provider = DeepAi
    elif site == "getgpt":
        provider = GetGpt
    elif site == "h2o":
        provider = H2o
    elif site == "huggingchat":
        provider = HuggingChat
    elif site == "opchatgpts":
        provider = Opchatgpts
    elif site == "openassistant":
        provider = OpenAssistant
    elif site == "openaichat":
        provider = OpenaiChat
    elif site == "raycast":
        provider = Raycast
    elif site == "theb":
        provider = Theb
    elif site == "vercel":
        provider = Vercel
    elif site == "wewordle":
        provider = Wewordle
    elif site == "wuguokai":
        provider = Wuguokai
    elif site == "you":
        provider = You
    elif site == "yqcloud":
        provider = Yqcloud
    else:
        provider = ChatgptAi

    model = request.get_json().get("model", "gpt-3.5-turbo")
    stream = request.get_json().get("stream", False)
    messages = request.get_json().get("messages")

    if not stream:
        # normal response
        response = g4f.ChatCompletion.create(
            model=model,
            messages=messages,
            provider=provider,
            stream=False,
        )

        completion_id = "".join(random.choices(string.ascii_letters + string.digits, k=28))
        completion_timestamp = int(time.time())
        return {
            "id": f"chatcmpl-{completion_id}",
            "object": "chat.completion",
            "created": completion_timestamp,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response,
                    }
                }
            ],
            "usage": {
                "prompt_tokens": None,
                "completion_tokens": None,
            }
        }
    else:
        return Response(streaming(
            model=model,
            messages=messages,
            provider=provider
        ), content_type='text/event-stream; charset=utf-8')
