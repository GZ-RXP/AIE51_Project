from services.BaseService import BaseService
from requests import request
import json

class NormService(BaseService):
    def __init__(self):
        self.url = ""


    def normalize(self, text, role, enable_norm=False):
        print(f"Normalization Service is running,role={role},input={text},enable_norm={enable_norm}")
        if enable_norm and role == "user": #仅对患者的输入进行判别
            data = {"user_input":text}
            try:
                response = request(method="POST",json=data , url=self.url)
                print(response.json()["symptom"])
                return response.json()["symptom"]
            except Exception as e:
                print("##ERROR when requesting Norm:",e)
                return "出错了，暂时无法判别症状，请稍后再试。"
        else:
            return ""