from task3_invoke_model import predict_by_Langchain
from flask import Flask, request, jsonify
import logging
import json

app = Flask(__name__)

@app.route('/get_symptom', methods=['POST'])
def get_dialogue_label():
    """
        接口名：/get_symptom
        请求body： {"user_input":"医生:嗓子红，现在不烧了，但有点咳嗽"}
        响应body：{"symptom":{'咽喉炎': '1','发热':'0','咳嗽','1'}}
    """
    data = request.get_json()
    logging.info(data)
    print(data)
    user_input = data['user_input']
    label = predict_by_Langchain(user_input=user_input)
    #处理字符，转json,再获取值
    #data = json.loads(label_str)
    #label = data['symptom']
    
    print(f"推理结果：{label}")
    return jsonify({'symptom': label})

app.run(host='0.0.0.0', port=5001)