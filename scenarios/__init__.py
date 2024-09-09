import os
import importlib
from .model import Scenario

def load_scenarios():
    scenarios = []
    scenario_files = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) 
                      if f.endswith('.py') and f != '__init__.py' and f != 'model.py']
    
    for scenario_file in scenario_files:
        module = importlib.import_module(f'.{scenario_file}', package='scenarios')
        if hasattr(module, 'scenario') and isinstance(module.scenario, Scenario):
            scenarios.append(module.scenario)

    difficulty_order = {"Easy": 1, "Medium": 2, "Hard": 3}
    return sorted(scenarios, key=lambda s: difficulty_order.get(s.difficulty, 4))

SCENARIOS = load_scenarios()

__all__ = ['SCENARIOS']
