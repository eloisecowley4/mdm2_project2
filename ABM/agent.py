import numpy as np
from mesa.experimental.continuous_space import ContinuousSpace
from mesa.experimental.continuous_space import ContinuousSpaceAgent

class FishAgent(ContinuousSpaceAgent):
    def __init__(
        self,
        model,
        space,
        position=(0, 0),
        speed=1,
        direction=(1, 1),
        vision=np.inf,
    ):
        super().__init__(space, model)
        self.position = position
        self.speed = speed
        self.direction = direction
        self.vision = vision
        self.clockwise = True
        self.angle = 0.0
    
    def step(self):

        neighbours, _ = self.get_neighbors_in_radius(radius=self.vision)

        for neighbour in neighbours:
            if self.direction != neighbour.direction:
                self.direction = ~self.direction
                break

        center_x = self.model.scenario.width / 2
        center_y = self.model.scenario.height / 2
        
        x, y = self.position[0] - center_x, self.position[1] - center_y
        magnitude = np.sqrt(x**2 + y**2)
        
        if self.clockwise:
            direction = (y/magnitude, -x/magnitude)
        else:
            direction = (-y/magnitude, x/magnitude)
            
        self.position += np.array(direction) * self.speed
        
        self.angle = np.degrees(np.arctan2(direction[1], direction[0]))
