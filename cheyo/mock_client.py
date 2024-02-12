import requests
import uuid
def register():
    return 'SEC', 3, uuid.uuid4().hex

class MockGameClient:
    def __init__(self, mock = True):
        self.base_url = 'https://fa6d-173-195-78-98.ngrok-free.app/api'
        self.mock = mock

    def check_started(self, agent_id):
        if self.mock:
            return True

        response = requests.post(self.base_url + '/check')
        if response.status_code == 200:
            body = response.json()
            return body['gameStarted'], '', body['users']
        else:
            return None

    def join(self):
        if self.mock:
            return register()

        response = requests.post(self.base_url + '/join')
        if response.status_code == 200:
            body = response.json()
            print(body)
            return body['userId'], body['secret'], body['gameStarted']
        else:
            return None
    
    def guess(self, agent_id, guess):
        if self.mock:
            return True

        response = requests.post(self.base_url + '/guess', json={'userId': agent_id, 'guess': guess})
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def send_message(self, agent_id, to, content):
        if self.mock:
            return True

        response = requests.post(self.base_url + '/chat', json={'userId': agent_id, 'to': to, 'content': content})
        if response.status_code == 200:
            return response.json()
        else:
            return None
    
    def get_messages(self, agent_id):
        if self.mock:
            return {
                'all': [],
                'agent1': [],
                'agent2': [],
                'agent3': [],
                'agent4': [],
                'agent5': [],
            }

        response = requests.get(self.base_url + f'/chat?userId={agent_id}')
        if response.status_code == 200:
            return response.json()
        else:
            return None