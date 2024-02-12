import requests
import uuid

class ChiyoGameClient:
    def __init__(self):
        self.base_url = 'http://testing-env.eba-uce6yjgk.us-east-1.elasticbeanstalk.com/api'

    def check_started(self, user_id):
        response = requests.get(self.base_url + f'/getkey?userId={user_id}')
        if response.status_code == 200:
            body = response.json()
            return body['success'], body.get('part', ''), body.get('participants', [])
        else:
            print(response)
            print(response.json())
            return None

    def join(self):
        id = uuid.uuid4().hex

        response = requests.post(self.base_url + '/join', json={'userId': id})
        print(response)
        if response.status_code == 200:
            body = response.json()
            return body['userId'], '', body['gameStarted']
        elif response.status_code == 403:
            print("Game full")
            print(response.json())
        else:
            return None
    
    def guess(self, agent_id, guess):
        response = requests.post(self.base_url + '/guess', json={'userId': agent_id, 'guess': guess})
        print('XXXXXXX Guess response', response)
        print(response.json())
        if response.status_code == 200:
            body = response.json()

            print('Guess response body', body)

            return body['success']
        else:
            print(response.json())
            return None
    
#     POST /api/dmchat
# - Description: Send a direct message.
# - Body: { "userId1": string, "userId2": string, "message": string }
# - Responses:
# - 200: Array<{ from: string, to: string, message: string }>
        
# 6. GET /api/dmchat
# - Description: Get direct message history.
# - Query: { "userId1": string, "userId2": string }
# - Responses:
# - 200: Array<{ from: string, to: string, message: string }>


    def send_message(self, agent_id, to, content):
        if to == 'all':
            response = requests.post(self.base_url + '/chat', json={'userId': agent_id, 'message': content})
            if response.status_code == 200:
                return response.json()
            else:
                print('error sending message', response)
                print(response.json())
                return None
        else:
            response = requests.post(self.base_url + '/dmchat', json={'userId1': agent_id, 'userId2': to, 'message': content})
            if response.status_code == 200:
                return response.json()
            else:
                print('error sending dm', response)
                print(response.json())
                return None
            
    def get_messages(self, user_id, others):
        all_messages = []
        dms = {}

        response = requests.get(self.base_url + f'/chat')
        if response.status_code == 200:
            body = response.json()
            if body['gameStarted'] == False:
                return None
            
            for message in body['chatHistory']:
                 all_messages.append({ 'from': message['userId'], 'content': message['message']})
        else:
            print('error getting messages', response)
            print(response.json())


        for other in others:
            response_dm = requests.get(self.base_url + f'/dmchat?userId1={user_id}&userId2={other}')
            if response.status_code == 200:
                body = response_dm.json()
                dms[other] = []
                for message in body:
                    dms[other].append({ 'from': message['from'], 'content': message['message']})
            else:
                print('error getting messages', response)
                print(response.json())
        
        dms['all'] = all_messages
        return dms


    def reset_game(self, user_id):
        response = requests.post(self.base_url + '/resetgame', json={'userId': user_id})
        if response.status_code == 200:
            return response.json()