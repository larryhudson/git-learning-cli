import json
import os
from pathlib import Path

HOME_DIR = str(Path.home())
COMPLETED_SCENARIOS_FILE = os.path.join(HOME_DIR, ".completed_git_scenarios.json")

def load_completed_scenarios():
    if os.path.exists(COMPLETED_SCENARIOS_FILE):
        with open(COMPLETED_SCENARIOS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_completed_scenarios(completed):
    with open(COMPLETED_SCENARIOS_FILE, 'w') as f:
        json.dump(completed, f)

def mark_scenario_completed(scenario_name):
    completed = load_completed_scenarios()
    completed[scenario_name] = True
    save_completed_scenarios(completed)

def is_scenario_completed(scenario_name):
    completed = load_completed_scenarios()
    return completed.get(scenario_name, False)
