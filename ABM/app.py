

import mesa.visualization as Mesa_Vis
from mesa.visualization.space_renderer import SpaceRenderer
from mesa.visualization.space_drawers import ContinuousSpaceDrawer
from mesa.visualization.backends import MatplotlibBackend

from model import FishScenario, FishTankModel
from agent import FishAgent
from matplotlib.pyplot import Axes
import matplotlib.pyplot as plt
import matplotlib.patches  as patch
import math

Scenario = FishScenario(
    # can make changes here to starting params
)

# RENDERING

def fish_draw(ax:Axes,agent:FishAgent):
    x,y = agent.pos
    ax.scatter(x,y,c='red')
    agent_bounds_arows(ax,agent)


def agent_bounds_arows(ax:Axes,agent:FishAgent) : 
    x,y = agent.pos
    colision = agent.boundry_ray_cast(agent.velocity,ax)
    dx,dy = colision - agent.pos
    arrow = patch.Arrow(x,y,dx,dy)
    direction = patch.Arrow(x,y,*agent.velocity,color='orange')
    ax.add_patch(arrow)
    ax.add_patch(direction)

def set_axies(ax:Axes) :
    ax.set_xlabel('X position (mm)')
    ax.set_ylabel(f'Y position (mm)')

def plot_boundrys(ax:Axes) :
    outer = patch.Circle((0,0),Scenario.outer_radius,fill=None,edgecolor='black')
    inner = patch.Circle((0,0),Scenario.inner_radius,fill=None,edgecolor='black')
    ax.add_patch(outer)
    ax.add_patch(inner)

def render(ax,model:FishTankModel) :

    set_axies(ax)
    plot_boundrys(ax)
    for agent in model.agents :
        fish_draw(ax,agent)

class SpaceRendererFish(SpaceRenderer) :

    def __init__(self,model,backend='matplotlib') :
        super().__init__(model,backend)
        self.backend_renderer = MatplotlibBackend(ContinuousSpaceDrawerFish(self.space))
        self.backend_renderer.initialize_canvas()
        

class ContinuousSpaceDrawerFish(ContinuousSpaceDrawer) :

    def draw_matplotlib(self, ax=None, **draw_space_kwargs):
        if ax is None:
            _, ax = plt.subplots()

        border_style = "solid" if not self.space.torus else (0, (5, 10))
        spine_kwargs = {"linewidth": 1.5, "color": "black", "linestyle": border_style}
        spine_kwargs.update(draw_space_kwargs)

        for spine in ax.spines.values():
            spine.set(**spine_kwargs)

        ax.set_xlim(self.viz_xmin, self.viz_xmax)
        ax.set_ylim(self.viz_ymin, self.viz_ymax)
        ax.set_aspect('equal')
        render(ax,model)

        return ax


# model setup

model = FishTankModel(Scenario)

model_params = {
    "scenario":Scenario,
}

renderer = SpaceRendererFish(model).render()

page = Mesa_Vis.SolaraViz(
    model,
    renderer,
    model_params=model_params,
    name="Fish Turning Model",
)