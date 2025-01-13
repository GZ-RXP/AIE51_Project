from predict_dialoge_dac import predict_by_Langchain
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route('/get_dialogue_label', methods=['POST'])
def get_dialogue_label():
    """
        接口名：/get_dialogue_label
        请求body： {"user_input":"医生:你好"}
        响应body：{"dialogue_label":"other"}
    """
    data = request.get_json()
    logging.info(data)
    print(data)
    user_input = data['user_input']
    label = predict_by_Langchain(user_input=user_input)
    print(f"推理结果：{label}")
    return jsonify({'dialogue_label': label})

app.run(host='0.0.0.0', port=5001)