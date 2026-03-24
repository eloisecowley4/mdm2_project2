import numpy as np
from mesa.experimental.continuous_space import ContinuousSpace
from mesa.experimental.continuous_space import ContinuousSpaceAgent

class FishAgent(ContinuousSpaceAgent):
    def __init__(
        self,
        model,
        space, 
        pos,
        direction=0,
        speed=1,
        vision=np.inf,
    ):
        super().__init__(space, model)
        self.pos = np.array(pos)
        self.speed = speed
        self.direction = direction
        self.vision = vision
    
    def step(self):
        self.direction += self.model.rng.uniform(-0.1, 0.1)

        look_ahead_dist = self.speed * 3

        future_x = self.pos[0] + np.cos(self.direction) * look_ahead_dist
        future_y = self.pos[1] + np.sin(self.direction) * look_ahead_dist

        while not self.model.is_in_ring((future_x, future_y)):
            self.direction += np.pi / 4 
            future_x = self.pos[0] + np.cos(self.direction) * look_ahead_dist
            future_y = self.pos[1] + np.sin(self.direction) * look_ahead_dist

        new_x = self.pos[0] + np.cos(self.direction) * self.speed
        new_y = self.pos[1] + np.sin(self.direction) * self.speed
        
        self.pos = np.array((new_x, new_y))
        