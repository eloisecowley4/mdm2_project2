import numpy as np
from mesa.experimental.continuous_space import ContinuousSpace
from mesa.experimental.continuous_space import ContinuousSpaceAgent
from dataclasses import dataclass


@dataclass
class AgentSettings() :

    # agent settings
    seperation_weight : float = 4.0 # NEEDS CHANGING
    seperation_range : float = 15.0 # based on analisis

    # DONE THE VALUES I GOT FOR 5 FISH - is that correct?
    coherence_weight : float = 3.81  
    coherence_range : float = 143.2 

    alignment_weight : float = .5 # NEEDS CHANGING
    alignment_range : float = coherence_range # might need changing

    bounds_weigth : float = 2.0 # needs changing
    bounds_range : float = 2.0 # needs changing

    speed_min : float = 3
    speed_max : float = 10

class FishAgent(ContinuousSpaceAgent):
    def __init__(
        self,
        model,
        space:ContinuousSpace , 
        position:np.typing.NDArray,
        settings:AgentSettings,
        velocity:np.typing.NDArray=np.array([1,1],dtype=float),
    ):
        super().__init__(space, model)

        self.position = position
        self.velocity = velocity
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

    def vec_2_wall_closest(self) :
    
        agent_r = np.sqrt(self.pos[0]**2 + self.pos[1]**2)

        # get radi
        inner_radius = self.model.scenario.inner_radius
        outer_radius = self.model.scenario.outer_radius

        # check outer wall
        dist_to_inner = abs(inner_radius - agent_r)
        dist_to_outer = abs(outer_radius - agent_r)

        if dist_to_inner < dist_to_outer :
            return self.pos * -(dist_to_inner/agent_r)
        else :
            return self.pos * (dist_to_outer/agent_r)
        
    def vec_2_wall_ahead(self) :

        pass

    def boundry_ray_cast(self,dir:np.typing.NDArray,ax) -> None|np.typing.NDArray :
        """returns the point of collision with the boundrys given a direction to cast a ray from the fish , returns None if no colision"""

        def check_collision(start:np.typing.NDArray,dir:np.typing.NDArray,radius:float) -> None|np.typing.NDArray :
            """checks if a ray, originating at (start) and in the direction (dir),
            collides with a circle with center at 0,0 and radius (raduis)
            returns None if no collision, otherwise the position of the collision"""

            # define the line
            m = (dir[1])/(dir[0])
            c = start[1] - m*start[0]

            # solve the quadratic 
            alpha = m**2 + 1
            beta = 2*m*c
            gamma = c**2 - radius**2

            descr = beta**2 - 4*alpha*gamma

            if descr < 0 : # no collision
                return None
            if descr == 0 : # 1 collision
                x = (-beta)/(2*alpha)

                # check if x is infront
                t = (x-start[0])/(dir[0])
                if t < 0 : # no colisions infront
                    return None

            else : # 2 collisions
                x1 = (-beta+np.sqrt(descr))/(2*alpha)
                x2 = (-beta-np.sqrt(descr))/(2*alpha)
                
                # check roots to make sure infront
                t1 = (x1-start[0])/(dir[0])
                t2 = (x2-start[0])/(dir[0])

                ax.scatter(x1,m*x1 + c,c='blue',label=f'{t1}')
                ax.scatter(x2,m*x2 + c,c='blue',label=f'{t2}')

                if t1 < 0 :
                    if t2 < 0 :
                        return None
                    else :
                        x = x2
                else :
                    if t2 < 0 :
                        x = x1
                    elif t1 < t2 :
                        x = x1
                    else : 
                        x = x2

            # use x to get y
            y = m*x + c
            ax.scatter(x,y,c='green')

            return np.array([x,y],dtype=float)
        
        inner_colision = check_collision(self.pos,dir,self.model.scenario.inner_radius)
        outer_colision = check_collision(self.pos,dir,self.model.scenario.outer_radius)

        # sort the collisions
        if inner_colision is None and outer_colision is None : 
            return None
        if inner_colision is None :
            return outer_colision
        if outer_colision is None :
            return inner_colision
        else : # check which colission is closest

            t_inner = (inner_colision[0]-self.pos[0])/(dir[0])
            t_outer = (outer_colision[0]-self.pos[0])/(dir[0])

            if t_inner < t_outer :
                return inner_colision
            else : 
                return outer_colision
        

    def bounds(self) :

        # check if wall is within view distance
        to_wall = self.vec_2_wall_closest()
        dist_to_wall = np.sqrt(to_wall[0]**2 + to_wall[1]**2)

        if dist_to_wall < self.settings.bounds_range :
            
            self.velocity += -to_wall * self.settings.bounds_weigth


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

        
