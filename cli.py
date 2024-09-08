# cli.py

import click
import os
import shutil
from pathlib import Path
from scenario import scenarios
from git_commands import run_git_command

HOME_DIR = str(Path.home())
REPO_PATH = os.path.join(HOME_DIR, "git_learning_repo")
CURRENT_SCENARIO_FILE = os.path.join(HOME_DIR, ".current_git_scenario")

@click.group()
def cli():
    """Git Learning CLI"""
    pass

def list_scenarios():
    """List all available scenarios"""
    click.echo("Available scenarios:")
    for idx, scenario in enumerate(scenarios, 1):
        click.echo(f"{idx}. {scenario['title']}")

def get_current_scenario():
    if os.path.exists(CURRENT_SCENARIO_FILE):
        with open(CURRENT_SCENARIO_FILE, 'r') as f:
            return f.read().strip()
    return None

def set_current_scenario(scenario_name):
    with open(CURRENT_SCENARIO_FILE, 'w') as f:
        f.write(scenario_name)

@cli.command()
@click.argument('scenario_name', required=False)
def start_scenario(scenario_name):
    """Start a specific scenario"""
    if not scenario_name:
        list_scenarios()
        scenario_number = click.prompt("Enter the number of the scenario you want to start", type=int)
        if 1 <= scenario_number <= len(scenarios):
            scenario_name = scenarios[scenario_number - 1]['title']
        else:
            click.echo("Invalid scenario number.")
            return

    scenario = next((s for s in scenarios if s['title'] == scenario_name), None)
    if not scenario:
        click.echo(f"Scenario '{scenario_name}' not found.")
        return

    # Delete the working folder if it exists
    if os.path.exists(REPO_PATH):
        shutil.rmtree(REPO_PATH)
    
    # Create a new working folder
    os.mkdir(REPO_PATH)

    # Initialize Git repository and create initial commit
    try:
        run_git_command(['init'], REPO_PATH)
        with open(os.path.join(REPO_PATH, 'README.md'), 'w') as f:
            f.write("# Git Learning Repository\n\nThis repository is for learning Git commands.\n")
        run_git_command(['add', 'README.md'], REPO_PATH)
        run_git_command(['commit', '-m', 'Initial commit'], REPO_PATH)
    except Exception as e:
        click.echo(f"Error initializing Git repository: {str(e)}")
        return

    try:
        scenario['generate_func'](REPO_PATH)
    except Exception as e:
        click.echo(f"Error generating scenario: {str(e)}")
        return

    set_current_scenario(scenario_name)

    click.echo(scenario['description'])
    click.echo(f"\nYour task: {scenario['task']}")
    click.echo(f"\nThe Git repository has been set up at: {REPO_PATH}")
    click.echo("This is a separate directory in your home folder to avoid conflicts with existing repositories.")
    click.echo("Once you've completed the task, use the 'check' command to verify your solution.")

@cli.command()
@click.argument('scenario_name', required=False)
def check(scenario_name):
    """Check the solution for a specific scenario"""
    if not scenario_name:
        scenario_name = get_current_scenario()
        if not scenario_name:
            click.echo("No active scenario found. Please start a scenario first.")
            return

    scenario = next((s for s in scenarios if s['title'] == scenario_name), None)
    if not scenario:
        click.echo(f"Scenario '{scenario_name}' not found.")
        return

    if not os.path.exists(REPO_PATH):
        click.echo("No active scenario found. Please start a scenario first.")
        return

    result = scenario['check_func'](REPO_PATH)

    if result:
        click.echo("Congratulations! You've successfully completed the task.")
    else:
        click.echo("Not quite right. Try again or use the 'hint' command for help.")

@cli.command()
@click.argument('scenario_name', required=False)
def hint(scenario_name):
    """Get a hint for a specific scenario"""
    if not scenario_name:
        scenario_name = get_current_scenario()
        if not scenario_name:
            click.echo("No active scenario found. Please start a scenario first.")
            return

    scenario = next((s for s in scenarios if s['title'] == scenario_name), None)
    if not scenario:
        click.echo(f"Scenario '{scenario_name}' not found.")
        return

    click.echo(scenario['hint'])

@cli.command()
def reset():
    """Reset the current scenario"""
    if os.path.exists(REPO_PATH):
        shutil.rmtree(REPO_PATH)
        if os.path.exists(CURRENT_SCENARIO_FILE):
            os.remove(CURRENT_SCENARIO_FILE)
        click.echo("The current scenario has been reset. Use the 'start_scenario' command to begin again.")
    else:
        click.echo("No active scenario found. Use the 'start_scenario' command to begin a new scenario.")

if __name__ == '__main__':
    cli()
