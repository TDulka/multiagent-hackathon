#%%
from chiyo_client import ChiyoGameClient
from agents import MyAgent
import time
import sys
import random

strategy = '' if len(sys.argv) < 2 else sys.argv[1]

print(strategy)

chi_client = ChiyoGameClient()
#%%
agent = MyAgent(chi_client, strategy)

agent.register()

print('Agent: ', agent.id)

#%%
for i in range(1000):
    started = agent.check_started()
    print(started)
    if started:
        break
    time.sleep(5)

#%%
for i in range(30):
    data, finished = agent.do_action()
    print(f'Finished: {finished}. AGENT {agent.id} does:\n', data)
    time.sleep(4 + random.randint(0, 4))
    if finished:
        break