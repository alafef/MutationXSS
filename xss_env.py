import gym
import sys
from gym import error, spaces, utils
import observation as obs
import actions as act
import numpy as np
from input_generator import InputGenerator
import crawler as cr
URL = "https://xss-game.appspot.com/level1/frame"


class XSSEnv(gym.Env):
    def __init__(self, start_url=URL, log_file_name="train_log.txt", source_file="success_payloads.txt"):

        print(start_url)
        self.root_url = start_url
        self.max_try = 100
        self.f = open(log_file_name, 'w')
        self.g = open(source_file, 'w')
        self.stepCounter = 0
        self.input_module = InputGenerator()
        self.action_size = act.ACTION_SIZE
        self.action_space = spaces.Discrete(self.action_size)
        self.state_size = obs.STATE_SIZE
        self.observation_space = spaces.Box(low=-1.0, high=float(self.max_try + 1),
                                            shape=(self.state_size,), dtype=np.float32)

        self.initial_status = np.zeros(self.state_size, dtype=np.float32)
        self.status = np.zeros(self.state_size, dtype=np.float32)
        self._observation = np.zeros(self.state_size, dtype=np.float32)
        self.action = -1

    def step(self, action):
        self.stepCounter += 1
        self.f.write("----------------STEPs--------------")
        self.f.write("action: " + str(action) + "\n")

        self.action = action
        generated_input, self.status = self.input_module.do_action(action)
        print(self.status)
        print("Step: ", self.stepCounter, " payload: ", generated_input)
        reward = 0
        check = 0
        #print(self.status)
        #cr.xss_crawl(URL, generated_input)
        # reward = 0
        # if generated_input.find("script"):
        #     self.status[obs.CONTAIN_SCRIPT_STRING] = 1
        # if generated_input.find("<script>"):
        #     self.status[obs.HTML_SCRIPT_TAG_USED] = 1
        # if generated_input.find("alert"):
        #     self.status[obs.ALERT_STRING] = 1
        # if generated_input.find("<") or generated_input.find(">"):
        #     self.status[obs.BRACKET] = 1
        # if self.status[obs.BRACKET] or self.status[obs.ALERT_STRING] or self.status[obs.HTML_SCRIPT_TAG_USED] or self.status[obs.CONTAIN_SCRIPT_STRING]:
        #     reward += 1
        # else:
        #     reward -= 1
        #

        done = False
        if self.status[obs.EVENT_ELEMENT] == 1:
            reward += 1
        if self.status[obs.BACKSLASH] == 1:
            reward += 1
        if self.status[obs.HTML_TAG_USED] == 1:
            reward += 1
        if self.status[obs.JS_PAYLOAD] == 1:
            reward += 1
        if self.status[obs.ATTRIBUTE_UPPER] == 1:
            reward += 1
        if self.status[obs.NO_WHITE_SPACE] == 1:
            reward += 1
        if self.status[obs.HTML_MEDIA_TAG_USED] == 1:
            reward += 2
        if self.status[obs.ATTRIBUTE_UPPER] == 1:
            reward += 1
        if self.status[obs.URL_ENCODING] == 1:
            reward += 1
        if self.status[obs.PREVIOUS_ACTION] == self.status[obs.CURRENT_ACTION]:
            reward -= 2
        if self.input_module.current_input == self.input_module.previous_input:
            reward -= 2
        # if self.input_module.previous_input == self.input_module.current_input:
        #     reward -= 7
        if self.status[obs.EVENT_ELEMENT] == 1 and self.status[obs.BACKSLASH] == 1 and \
                self.status[obs.HTML_MEDIA_TAG_USED] == 1 and self.status[obs.ATTRIBUTE_UPPER] == 1 and \
                self.status[obs.URL_ENCODING] == 1 and self.status[obs.HTML_TAG_USED] == 1 and \
                self.status[obs.NO_WHITE_SPACE] ==1 and self.status[obs.JS_PAYLOAD] == 1:
            self.status[obs.ATTACK_SUCCESS] = 1
            done = True
            self.g.write(generated_input + "\n")

                #raise RuntimeError("SUCCESS")
            reward += 10
        else:
            reward -= 10
        print(reward)
        print(done)
        #self._observation = self.status
        #print(self._observation)
        return self.status, reward, done, {} #self._observation

    def reset(self):
        self.stepCounter = 0
        found = False

        self._observation = self.initial_status
        print("initial status " + str(self.initial_status))
        return self._observation

    def render(self):
        pass


