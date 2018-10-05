from gym.envs.registration import register

register(
    id='ReacherMy-v0',
    entry_point='reacher.Reacher:ReacherEnv',
)
