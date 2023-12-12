import openai
import langchain as lc
from langchain.llms import OpenAI
import gradio as gr

# 设置OpenAI API密钥
openai.api_key = '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'

# 初始化Langchain的OpenAI LLM
llm = OpenAI(api_key=openai.api_key)


# 定义一个函数来处理上传的文档并生成响应
def process_document(document):
    # 这里可以添加代码来处理文档，例如提取文本、向量化等
    text = document.read()

    # 使用GPT-3.5生成响应
    response = llm.generate(text)

    return response


# 创建Gradio界面
iface = gr.Interface(
    fn=process_document,
    inputs=gr.inputs.File(label="上传文档"),
    outputs="text",
    title="基于GPT-3.5和Langchain的知识库",
    description="上传文档以获取GPT-3.5生成的响应"
)

# 运行Gradio应用
iface.launch()
