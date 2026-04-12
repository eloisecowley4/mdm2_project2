import numpy as np
from mesa.experimental.continuous_space import ContinuousSpace
from mesa.experimental.continuous_space import ContinuousSpaceAgent

class FishAgent(ContinuousSpaceAgent):
    def __init__(
        self,
        model,
        space:ContinuousSpace , 
        position:np.typing.NDArray,
    ):
        super().__init__(space, model)

        self.position = position
        self.velocity = np.array([0,0],dtype=float)

    def update(self) :
        '''
        figures out the how to change the movement
        '''
        self.velocity = np.array([1,1],dtype=float)
        pass

    def step (self) :
        '''update based on diffrences'''

        self.update()
        # update position
        self.position += self.velocity

        