import http.client
import json
import proxy

proxy.proxy()

conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
payload = json.dumps({
    "contents": [
        {
            "parts": [
                {
                    "text": "帮我解析一下这个网页：https://github.com/google/generative-ai-python/issues/118"
                }
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
})
headers = {
    'Content-Type': 'application/json'
}
conn.request("POST", "/v1beta/models/gemini-pro:generateContent?key=AIzaSyCzLBBh243bcKndgYuByv9PUygjMEaTSJk", payload,
             headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

conn.close()
