from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# 加载embedding
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec2": "uer/sbert-base-chinese-nli",
    "text2vec3": "shibing624/text2vec-base-chinese",
    "text2vec3-local": r"D:\gpt-chain\res\shibing624\text2vec-base-chinese",
}


def load_embedding_model(model_name="ernie-tiny"):
    encode_kwargs = {"normalize_embeddings": False}
    model_kwargs = {"device": "cuda:0"}
    return HuggingFaceEmbeddings(
        model_name=embedding_model_dict[model_name],
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )


print("加载数据库...", end='\r', flush=True)
embeddings = load_embedding_model('text2vec3-local')
db = Chroma(persist_directory='VectorStore', embedding_function=embeddings)
print("数据库加载完成.")


def search(question, num=4):
    print(f"相似查询: {question}")
    return db.similarity_search(question, k=num)
