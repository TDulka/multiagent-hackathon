# multiagent-hackathon
Simple repo developed during a hackathon.

`cheyo-server` has a simple mock api for testing

`cheyo` contains a setup for simple agents playing a game

Run `cheyo/spawn_agents n` to spawn n agents, they sample from a list of strategies defined in that file.

Requires OpenAI API key located in `cheyo/keys.json` in the format:

```
{
    "openai": YOUR_KEY_HERE
}
```