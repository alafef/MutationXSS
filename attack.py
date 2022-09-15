import sys
import gym
import xss_env
from stable_baselines3.a2c.policies import MlpPolicy
from stable_baselines3 import A2C
import warnings
import tensorflow as tf

warnings.simplefilter(action='ignore', category=FutureWarning)
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

gym.envs.register(
     id='xss_env-v0',
     entry_point='xss_env:XSSEnv',
     max_episode_steps=1000,
)

def main(argv):
    start_url = ""

    # create the environment
    env = gym.make("xss_env-v0", start_url=start_url)
    # create learning agent
    print("[*] Loading A2Cmodel ...")

    model = A2C.load("model.pkl")
    print("[*] Start Agent working ...")
    obs = env.reset()
    h = open("attack_payloads.txt", 'w')
    attack_step = 0
    while True:
        attack_step += 1
        action, _states = model.predict(obs)

        obs, rewards, done, info = env.step(action)
        print(obs)
        print("ATTACK STEP: ", attack_step)
        env.reset()
        if done:
            #h.write(info + "\n")
            env.reset()
            break
    h.close()


if __name__ == '__main__':
    main(sys.argv)