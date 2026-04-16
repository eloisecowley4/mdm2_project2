#Define the fishtank in here 
import numpy as np
from mesa import Model
from mesa.experimental.continuous_space import ContinuousSpace
from agent import FishAgent, AgentSettings
from dataclasses import dataclass

@dataclass
class FishScenario:
    n_fish: int = 2
    speed: float = 1.0
    seed: int = 42

    #I think this is wrong/ should be moved into the fish tank model
    #Job for later, only do when/if change away from ring boundary
    width: int = 100
    height: int = 100
    inner_radius: float = 20.0
    outer_radius: float = 45.0


class FishTankModel(Model):    
    def __init__(self,scenario:FishScenario,**kwargs):
        '''
        Initialise the space for the ring model

        '''

        # load senario settings
        self.scenario = scenario

        super().__init__(seed=self.scenario.seed)

        # make the space the fish are in
        self.space = ContinuousSpace(
            [
            [-self.scenario.width/2,self.scenario.width/2], # x axis
            [-self.scenario.height/2,self.scenario.height/2] # y axis
            ], 
            torus=False,
            random=self.rng
            )

        #set center to be 0.0
        self.centre = (0.0,0.0)

        # add agents
        self._setup_agents()
    
    def _setup_agents(self):
        '''
        Initializes positions of agents 
        '''
        n = self.scenario.n_fish

        positions = []

        for _ in range(n) :
            angle = self.rng.random()*np.pi*2 # random angle
            radius = self.scenario.inner_radius + self.rng.random()*(self.scenario.outer_radius - self.scenario.inner_radius)
            pos = np.array([radius*np.cos(angle),radius*np.sin(angle)])
            positions.append(pos)
            

        FishAgent.create_agents(
                model=self, 
                n=self.scenario.n_fish,
                space=self.space,
                position=positions,
                settings=AgentSettings(),
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