from flask import Flask, render_template, request
from db import search
import json

app = Flask(__name__)


@app.route('/')
def app_home():
    return render_template('./index.html', results=[])


@app.route('/search')
def app_search():
    question = request.args.get('question')
    num = int(request.args.get('num'))
    results = search(question, num=num)
    return render_template('./index.html', results=results, question=question, num=num)


@app.route('/search_api')
def app_search_api():
    question = request.args.get('question')
    num = int(request.args.get('num'))
    results = search(question, num=num)
    return json.dumps([doc.__dict__ for doc in results], ensure_ascii=False)


if __name__ == '__main__':
    app.run()
