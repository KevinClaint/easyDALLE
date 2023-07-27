import openai
from flask import Flask, request, jsonify, render_template, Response
import os

app = Flask(__name__)

# 从配置文件中settings加载配置
app.config.from_pyfile('settings.py')
openai.api_key = os.environ.get('OPENAI_API_KEY',app.config["OPENAI_API_KEY"])

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    messages = request.form.get("user_input", None)
    if messages is None:
        return jsonify({"error": {"message": "请输入prompts！", "type": "invalid_request_error", "code": ""}})

    # json串转对象
    completion = openai.Image.create(
        prompt=messages,
         n=1,
        size="512x512"
    )
    reply=completion["data"][0]["url"]

    return render_template('index.html', image_path=reply)

if __name__ == '__main__':
    app.run(port=5000)