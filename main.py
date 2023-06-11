import random

class MyEnvironment:

    def __init__(self):
        self.remaining_steps = 20

    def get_observation(self):
        return [1.0, 2.0, 1.0]

    def get_actions(self):
        return [-1, 1]

    def check_is_done(self):
        return self.remaining_steps == 0

    def action(self, ac):
        if self.check_is_done():
            raise Exception("Game over")
        self.remaining_steps -= 1
        return random.random()
    
class myAgent:
    def __init__(self):
        self.total_rewards = 0.0

    def step(self, ob: MyEnvironment):
        curr_obs = ob.get_observation()
        print(curr_obs)
        curr_action = ob.get_actions()
        print(curr_action)
        curr_reward = ob.action(random.choice(curr_action))
        self.total_rewards += curr_reward
        print("Total rewards so far= %.3f "%self.total_rewards)

if __name__=='__main__':
    obj = MyEnvironment()
    agent=myAgent()
    step_number=0
    while not obj.check_is_done():
        step_number+=1
        print("Step-",step_number)
        agent.step(obj)
    print("Total reward is %.3f "%agent.total_rewards)