import g4f
import gradio as gr
import time
import os
from transformers import Conversation
from db import search_contents

# Print all available providers
print([
    provider.__name__
    for provider in g4f.Provider.__providers__
    if provider.working
])


# prompt = "\n\n--提示词：请尝试理解我的问题，翻译为英语之后再进行解答，最后将输出翻译为汉语，谢谢\n\n"

def chat(content):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        provider=g4f.Provider.PerplexityAi,
        messages=[{"role": "user", "content": content}],
        proxy="http://127.0.0.1:10809",
        # stream=True,
    )

    return ''.join(msg for msg in response)


def add_text(history, text):
    history = history + [(text + "\n\n请根据以下参考内容回答上述问题：\n" + search_contents(text, num=8), None)]
    return history, gr.update(value="", interactive=False)


def add_file(history, file):
    """
    上传文件后的回调函数，将上传的文件向量化存入数据库
    :param history:
    :param file:
    :return:
    """
    # global qa
    # directory = os.path.dirname(file.name)
    # documents = load_documents(directory)
    # db = store_chroma(documents, embeddings)
    # retriever = db.as_retriever()
    # qa.retriever = retriever
    # history = history + [((file.name,), None)]
    return history


def bot(history):
    """
    聊天调用的函数
    :param history:
    :return:
    """
    message = history[-1][0]
    if isinstance(message, tuple):
        response = "文件上传成功！！"
    else:
        response = chat(message)
    history[-1][1] = response
    yield history
    # for character in response:
    #     history[-1][1] += character
    #     yield history


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=True,
        height=1000,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),

    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
            lines=2,
        )
        btn = gr.UploadButton("📁", file_types=['txt'])

    txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )

demo.launch()
