from requests import request

def get_symptom(text):
    url = "http://direct.virtaicloud.com:48053/get_symptom"
    data = {"user_input":text}
    response = request(method="POST",json=data , url=url)
    print(response.json())

def get_intent(text):
    url = "http://direct.virtaicloud.com:26177/get_dialogue_label"
    data = {"user_input":text}
    response = request(method="POST",json=data , url=url)
    print(response.json())

if __name__ == "__main__":
    get_symptom("有没有流鼻涕？")
    get_intent("医生：你好")