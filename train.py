import gym
import sys
import xss_env
from stable_baselines3.a2c.policies import MlpPolicy, CnnPolicy
from stable_baselines3 import A2C
import torch as th
import warnings
import tensorflow as tf
warnings.simplefilter(action='ignore', category=FutureWarning)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

gym.envs.register(
     id='xss_env-v0',
     entry_point='xss_env:XSSEnv',
     max_episode_steps=1000,
)

seed = 1234
tf.random.set_seed(seed)


def main(argv):
    start_url = "https://xss-game.appspot.com/level1/frame"
    timesteps = 40000

    env = gym.make("xss_env-v0", start_url=start_url)

    # create learning agent
    print("[*] Creating A2C model ...")
    policy_kwargs = dict(activation_fn=th.nn.ReLU, net_arch=[dict(pi=[128, 128, 128], vf=[128, 128, 128])])

    learning_rate = 0.0005
    gamma = 0.95
    model = A2C(MlpPolicy, env, verbose=1, learning_rate=learning_rate,
                gamma=gamma)
    print("[*] Start Agent learning ...")

    model.learn(total_timesteps=timesteps)

    model.save("model.pkl")

    del model


if __name__ == '__main__':
    main(sys.argv)