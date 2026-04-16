import numpy as np
from mesa.experimental.continuous_space import ContinuousSpace
from mesa.experimental.continuous_space import ContinuousSpaceAgent
from dataclasses import dataclass


@dataclass
class AgentSettings() :

    # agent settings
    seperation_weight : float = 1.0 # NEEDS CHANGING
    seperation_range : float = 15.0 # based on analisis

    # DONE THE VALUES I GOT FOR 5 FISH - is that correct?
    coherence_weight : float = 3.81  # NEEDS CHANGING 
    coherence_range : float = 143.2 # NEEDS CHANGING

    alignment_weight : float = .5 # NEEDS CHANGING
    alignment_range : float = coherence_range # might need changing

    bounds_weigth : float = 2.0 # needs changing
    bounds_range : float = 5.0 # needs changing

    speed_min : float = 3
    speed_max : float = 10

class FishAgent(ContinuousSpaceAgent):
    def __init__(
        self,
        model,
        space:ContinuousSpace , 
        position:np.typing.NDArray,
        settings:AgentSettings,
    ):
        super().__init__(space, model)

        self.position = position
        self.velocity = np.array([0,0],dtype=float)
        self.model = model
        self.settings = settings

    def seperation(self) :
        neigbours, dist = self.get_neighbors_in_radius(self.settings.seperation_range)

        if len(neigbours) == 0 : return

        move = np.array([0.0,0.0])
        for i, other in enumerate(neigbours) :
            move += self.position - other.position

        self.velocity += move * self.settings.seperation_weight * self.dt

    def coherence(self) :
        neigbours, dist = self.get_neighbors_in_radius(self.settings.coherence_range)
        
        if len(neigbours) == 0 : return

        center_of_mass = np.array([0.0,0.0])
        for other in neigbours :
            center_of_mass += other.position
        center_of_mass /= len(neigbours)

        self.velocity += (center_of_mass - self.position) * self.settings.coherence_weight  * self.dt

        pass

    def alignment(self) :
        neigbours, dist = self.get_neighbors_in_radius(self.settings.alignment_range)

        if len(neigbours) == 0 : return

        average_velocity = np.array([0.0,0.0])
        for other in neigbours :
            average_velocity += other.velocity
        average_velocity /= len(neigbours)

        self.velocity += (average_velocity - self.velocity) * self.settings.alignment_weight  * self.dt

        pass

    def bounds(self) :
        pass

    def speed(self) : 
        speed = np.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        self.velocity /= speed

        speed = max(self.settings.speed_min,min(self.settings.speed_max,speed))
        
        self.velocity *= speed
        pass

    def update(self) :
        '''
        figures out the how to change the movement
        '''
    
        # step 1 : Seperation 
        self.seperation()

        # step 2 : coherence
        self.coherence()

        # step 3 : alignment 
        self.alignment()
        
        # step 4 boundry avodiance 
        self.bounds()

        # cap speed
        self.speed()


    def step (self) :
        '''update based on diffrences'''
        self.dt = 1/50 # need to make this bassed on somthing
        self.update()
        # update position
        self.position += self.velocity * self.dt

        