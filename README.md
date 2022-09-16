# MutationXSS
## Train
Just run train.py without options.
Below you see:
1. Observation space (Matrix of mutations) - generated on key elements of each payload such as quotation, url encoding, brackets, no white spaces etc.
(You need to check file observation.py to understand this matrix)
2. Step of environment and action (payload) generated at this step
3. Reward
4. Resulf of attack (True or False)
![image](https://user-images.githubusercontent.com/78353932/190605412-906bd87e-f8d8-4b2b-8ef7-046a66b9cba2.png)

It will build model.pkl
## Attack
Run attack.py without options (It will attack based on builded model.pkl)
![image](https://user-images.githubusercontent.com/78353932/190604034-13e2c310-b19b-4d6c-ac83-dd9323919bba.png)
