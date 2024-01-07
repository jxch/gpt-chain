import http.client
import json
import proxy

proxy.proxy()

conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
key = "AIzaSyCzLBBh243bcKndgYuByv9PUygjMEaTSJk"

param = {
    "contents": [
        {
            "parts": [
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.9,
        "topK": 1,
        "topP": 1,
        "maxOutputTokens": 2048,
        "stopSequences": []
    },
    "safetySettings": [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        }
    ]
}

headers = {
    'Content-Type': 'application/json'
}


def query(question):
    param["contents"][0]["parts"].append({"text": question})
    conn.request("POST", "/v1beta/models/gemini-pro:generateContent?key=" + key,
                 json.dumps(param), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    res_obj = eval(data.decode("utf-8"))
    if res_obj["candidates"][0]["finishReason"] == "STOP":
        text = res_obj["candidates"][0]["content"]["parts"][0]["text"]
        conn.close()

        if "citationMetadata" in res_obj["candidates"][0]:
            text += "\n\n关于本段回答参考资料：\n"
            for item in res_obj["candidates"][0]["citationMetadata"]["citationSources"]:
                text += item["uri"] + "\n"

        return text



