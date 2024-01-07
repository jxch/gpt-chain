import g4f
import gradio as gr
import time
import os
from transformers import Conversation
from db import search_contents
from gmini import query
import roles


def chat(content):
    res = query(content)
    if res:
        return ''.join(msg for msg in res)
    else:
        return ''.join(msg for msg in "稍等")


def add_text(history, text):
    history = history + [("\n\n请根据以下参考内容回答这个问题：" + text + "\n\n" + search_contents(text, num=8), None)]
    return history, gr.update(value="", interactive=False)


def his_text(history, text, role_name):
    text, history = roles.add_role_text(text, history, role_name)
    history = history + [(text, None)]
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


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=True,
        height=1000,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        role = gr.Dropdown(choices=["默认", "编程助手"], show_label=False)
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
            lines=2,
        )
        pa_btn = gr.Button("知识库")
        btn = gr.UploadButton("📁", file_types=['txt'])

    txt_msg = txt.submit(his_text, [chatbot, txt, role], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot
    )
    txt_msg.then(lambda: gr.update(interactive=True), None, [txt], queue=False)
    file_msg = btn.upload(add_file, [chatbot, btn], [chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    pa_btn.click(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
        bot, chatbot, chatbot).then(lambda: gr.update(interactive=True), None, [txt], queue=False)

demo.launch()
