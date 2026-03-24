#Define the fishtank in here 
import numpy as np
from mesa import Model
from mesa.experimental.continuous_space import ContinuousSpace
from agent import FishAgent
from dataclasses import dataclass

@dataclass
class FishScenario:
    n_fish: int = 2
    speed: float = 1.0

    #I think this is wrong/ should be moved into the fish tank model
    #Job for later, only do when/if change away from ring boundary
    width: int = 100
    height: int = 100
    inner_radius: float = 20.0
    outer_radius: float = 45.0

class FishTankModel(Model):    
    def __init__(self, n_fish=2, speed=1.0, width=100, height=100, seed=None):
        '''
        Initialise the space for the ring model
        '''
        super().__init__(seed=seed)

        self.scenario = FishScenario(
            n_fish=n_fish, 
            speed=speed, 
            width=width, 
            height=height
        )

        self.space = ContinuousSpace(
            [[0, self.scenario.width], [0, self.scenario.height]], 
            torus=False,
            random=self.rng
    )

        self.centre = (self.scenario.width/2, self.scenario.height/2)

        self._setup_agents()
    
    def _setup_agents(self):
        '''
        Vectorized initialization of agents: calculates all starting pos 
        and directions at once before instantiating the agents.
        '''
        n = self.scenario.n_fish
        initiation_radius = (self.scenario.inner_radius + self.scenario.outer_radius) / 2

        initiation_angles = self.rng.random(n) * np.pi * 2
        directions = self.rng.random(n) * np.pi * 2

        x_pos = np.cos(initiation_angles) * initiation_radius + self.centre[0]
        y_pos = np.sin(initiation_angles) * initiation_radius + self.centre[1]

        FishAgent.create_agents(
                model=self, 
                n=self.scenario.n_fish,
                space=self.space,
                pos=(x_pos, y_pos),
                direction=directions,
                speed=self.scenario.speed
            )

    def is_in_ring(self, pos):
        '''
        Function to check if a pos of a fish is within the ring
        '''
        x, y = pos

        centre_x, centre_y = self.centre

        dist = np.sqrt((x - centre_x)**2 + (y - centre_y)**2)

        return self.scenario.inner_radius <= dist <= self.scenario.outer_radius

    def step(self):
        self.agents.shuffle_do("step")