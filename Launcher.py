from tree import Agent

agent = Agent(
    size = 15,
    win_len = 5,
    max_searches = 10000
)
agent.play_with_human()
