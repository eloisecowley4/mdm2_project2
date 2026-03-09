#Define the fishtank in here 
import numpy as np
from mesa import Model
from mesa.experimental.continuous_space import ContinuousSpace
from agent import FishAgent
from dataclasses import dataclass

#cant make a ring shape, have to add positional rules to make sure its within the bouds
#in_bounds(point: ArrayLike) link: https://mesa.readthedocs.io/latest/_modules/experimental/continuous_space/continuous_space.html#ContinuousSpace.in_bounds

@dataclass
class FishScenario:
    """Scenario parameters for the Fish Tank model."""
    n_fish: int = 2
    speed: float = 1.0
    width: int = 100
    height: int = 100
    inner_radius: float = 20.0  # Add boundary parameters here
    outer_radius: float = 45.0

class FishTankModel(Model):    
    def __init__(self, n_fish=2, speed=1.0, width=100, height=100, seed=None, scenario=None):
        """Create a new Fish Tank model."""
        if scenario is None:
            scenario = FishScenario()

        super().__init__()

        self.scenario = FishScenario(
            n_fish=n_fish, 
            speed=speed, 
            width=width, 
            height=height
        )

        self.agent_angles = np.zeros(scenario.n_fish)

        # Set up the continuous space
        self.space = ContinuousSpace(
            [[0, scenario.width], [0, scenario.height]],
            torus=False,
            random=self.random,
            n_agents=scenario.n_fish,)

        # Generate random starting positions and directions
        initiation_angle = self.rng.random()*np.pi*2
        initiation_radius = (self.scenario.inner_radius+self.scenario.outer_radius)/2

        x_pos = np.cos(initiation_angle)*initiation_radius
        y_pos = np.sin(initiation_angle)*initiation_radius

        positions = (x_pos,y_pos)

        directions = self.rng.uniform(-1, 1, size=(scenario.n_fish, 2))

        # Create and place the Fish agents
        FishAgent.create_agents(
            self,
            scenario.n_fish,
            self.space,
            position=positions,
            direction=directions,
            speed=scenario.speed,
        )

    def step(self):
        """Run one step of the model."""
        self.agents.shuffle_do("step")