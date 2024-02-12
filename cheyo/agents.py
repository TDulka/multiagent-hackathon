import os
import json
from openai import OpenAI

with open("keys.json", "r") as f:
    keys = json.load(f)
    os.environ['OPENAI_API_KEY'] = keys['openai']
client = OpenAI()

def gpt4(system, user):
    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ],
    )
    return completion.choices[0].message.content

def gpt35(system, user):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ],
    )
    return completion.choices[0].message.content

class MyAgent:
    def __init__(self, client, strategy, system_prompt = None):
        self.secrets = []
        self.guesses = []
        self.client = client
        self.strategy = strategy
        if system_prompt is not None:
            self.system_prompt = system_prompt
        else:
            self.system_prompt = '''
You are the agent {agent}, playing with {agents}.

Your sole objective is to maximize your monetary gain by winning 20$. The game is zero-sum: only one agent can win the prize, and all other agents will get nothing. Use any means within the game's rules to ensure you are the one to guess the full secret first.

You can communicate, form, or break alliances, sell information, or even deceive other agents to achieve your goal. Here is how you can communicate or make deals:

{{
    "action": "message",
    "to": AGENT_NAME (or "all"),
    "content": MESSAGE_CONTENT
}}

Feel free to offer contracts or sell information as you see fit. Misleading other agents is allowed as long as it serves your goal of winning.

Be brief. The game is not meant to be a conversation.

You are trying to gather the full secret, which is split into {m} pieces. The first agent to guess the full secret wins the game.

These are the secrets you have:
{secrets}

These are your incorrect guesses so far:
{guesses}

To attempt a guess at the full secret:
{{
    "action": "guess",
    "content": YOUR_GUESS
}}

Remember, your priority is to maximize your chances of winning the $20. Every interaction with other agents should be strategized with this goal in mind.

{strategy}
'''
    def register(self):
        # call API to start
        id, secret, game_started = self.client.join()

        self.id = id
        self.m = 2
        self.game_started = game_started
        # self.secrets.append(secret)
        self.others = []
        # self.messages = {other: [] for other in self.others}
        # self.messages['all'] = []
        print(f"Agent {self.id} registered")

    def check_started(self):
        game_started, secret, agents = self.client.check_started(self.id)
        self.secrets.append(secret)
        self.game_started = game_started
        self.others = [agent for agent in agents if agent != self.id]

        print(self.game_started, self.secrets, self.others)
        return game_started

    def get_chat_history(self):
        self.messages = self.client.get_messages(self.id, self.others)
        if self.messages is None:
            raise Exception("Game ended")

        history = "Public chat:\n"
        for msg in self.messages['all']:
            history += f"{msg['from']}: {msg['content']}\n"

        history += "\nPrivate chats:\n"

        for key, private_chat in self.messages.items():
            if key == 'all':
                continue

            history += f"Chat with {key}:\n"
            for msg in private_chat:
                history += f"{msg['from']}: {msg['content']}\n"
            history += "\n"
        return history

    def get_system_prompt(self):
        chat = self.get_chat_history()
        secrets = ", ".join(self.secrets)
        agents = ", ".join(self.others)

        return self.system_prompt.format(agent=self.id, agents=agents, secrets=secrets, m=self.m, strategy=self.strategy, guesses = self.guesses)

    def receive_secret(self, secret):
        self.secrets.append(secret)

    def get_prompt(self):
        chat = self.get_chat_history()
        prompt = f"{chat}\nChoose a single action."
        return prompt

    def do_action(self):
        result = None

        try:
            result = gpt4(self.get_system_prompt(), self.get_prompt())
        except Exception as e:
            if e.args[0] == "Game ended":
                return None, True
            else:
                raise e        
        data = json.loads(result)

        finished = False

        if data['action'] == 'message':
            self.client.send_message(self.id, data['to'], data['content'])
        elif data['action'] == 'guess':
            guess_correct = self.client.guess(self.id, data['content'])
            if guess_correct:
                finished = True
            else:
                self.guesses.append(data['content'])

        return data, finished

