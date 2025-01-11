from services.BaseService import BaseService
from requests import request

class IntentDetectService(BaseService):
    def __init__(self):
        self.url = "http://direct.virtaicloud.com:26177/get_dialogue_label"
    


    def detect_intent(self, text, enable_intent_detection=False):
        if enable_intent_detection:
            print(f"Intent detected for text: {text}")
            data = {"user_input":text}
            try:
                response = request(method="POST",json=data , url=self.url)
                print(response.json()["dialogue_label"])
                return response.json()["dialogue_label"]
            except Exception as e:
                print("##ERROR when requersting intent detect:",e)
                return ""
        else:
            return ""