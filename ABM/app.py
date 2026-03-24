from matplotlib.markers import MarkerStyle

from mesa.visualization.components import AgentPortrayalStyle
from mesa.visualization import Slider, SolaraViz, SpaceRenderer
from dataclasses import dataclass
from model import FishScenario, FishTankModel

def fish_draw(agent):
    fish_style = AgentPortrayalStyle(
        color="red", size=20, marker=MarkerStyle(10)
    )
    return fish_style

model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "n_fish": Slider(
        label="Number of Fish",
        value=2,
        min=1,
        max=5,
        step=1,
    ),
    "width": 100,
    "height": 100,
    "speed": Slider(
        label="Speed of Fish",
        value=5,
        min=1,
        max=20,
        step=1,
    ),
}
model = FishTankModel()

renderer = (
    SpaceRenderer(
        model,
        backend="matplotlib",
    )
    .setup_agents(fish_draw)
    .render()
)

page = SolaraViz(
    model,
    renderer,
    model_params=model_params,
    name="Fish Turning Model",
)
page