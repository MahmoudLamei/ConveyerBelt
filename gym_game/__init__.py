from gymnasium.envs.registration import register

register(
    # Envinoment ID
    id='Pygame-v0',
    # Entry point which is the env class
    entry_point='gym_game.envs:CustomEnv',
    # Setting a maximum number of episodes to run
    max_episode_steps=2000,
)
