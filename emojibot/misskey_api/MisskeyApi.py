from .model import *
from .exception import *
import requests
import json

class MisskeyApi:

    def __init__(self, host, token):
        self.host = host
        self.base_url = f"https://{host}/api/"
        self.token = token

    def request_api(self, endpoint, params):
        r  = requests.post(f"{self.base_url}{endpoint}", json=params)
        return r

    def show_user(self):
        params ={
            "i": self.token
        }
        r  = self.request_api("i", params)
        if r.status_code != 200:
            raise BadApiRequestException(r.status_code, r.text)
        return User(json.loads(r.text))
        
    def create_note(self, text, cw = None, visibility = "public", localOnly = True, reactionAcceptance = None):
        params ={
            "i": self.token,
            "text": text,
            "cw" : cw,
            "visibility": visibility,
            "localOnly":  localOnly,
            "reactionAcceptance": reactionAcceptance,
        }
        r  = self.request_api("notes/create", params)
        if r.status_code != 200:
            raise BadApiRequestException(r.status_code, r.text)
       
    def show_moderation_logs(self, limit = 5, type = None, sinceId = None, untilId = None, userId = None):
        params ={
            'i': self.token,
            'limit': limit,
            'type': type,
            'userId': userId
        }
        if sinceId is not None:
            params["sinceId"] = sinceId
        if untilId is not None:
            params["untilId"] = untilId
        r  = self.request_api("admin/show-moderation-logs", params)
        if r.status_code != 200:
            raise BadApiRequestException(r.status_code, r.text)
        array = json.loads(r.text)
        moderation_logs = []
        for i in array:
            moderation_logs.append(ModerationLog(i))
        return moderation_logs



