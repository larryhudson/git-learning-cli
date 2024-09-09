# cli.py

import click
import os
import shutil
from pathlib import Path
from scenarios import SCENARIOS
from git_commands import run_git_command
from completed_scenarios import mark_scenario_completed, is_scenario_completed

HOME_DIR = str(Path.home())
REPO_PATH = os.path.join(HOME_DIR, "git_learning_repo")
CURRENT_SCENARIO_FILE = os.path.join(HOME_DIR, ".current_git_scenario")

@click.group()
def cli():
    """Git Learning CLI"""
    pass

def list_scenarios(difficulty=None):
    """List all available scenarios"""
    click.echo("Available scenarios:")
    for idx, scenario in enumerate(SCENARIOS, 1):
        if difficulty is None or scenario.difficulty == difficulty:
            completed = "✓" if is_scenario_completed(scenario.title) else " "
            click.echo(f"{idx}. [{completed}] {scenario.title} (Difficulty: {scenario.difficulty})")

def display_scenario_info():
    """Display detailed information about all scenarios"""
    for idx, scenario in enumerate(SCENARIOS, 1):
        completed = "✓" if is_scenario_completed(scenario.title) else " "
        click.echo(f"\n{idx}. [{completed}] {scenario.title}")
        click.echo(f"   Difficulty: {scenario.difficulty}")
        click.echo(f"   Description: {scenario.description}")
        click.echo(f"   Task: {scenario.task}")
        click.echo("   " + "-" * 40)

@cli.command()
@click.option('--scenario', '-s', type=str, help='The scenario to mark as completed')
@click.option('--info', '-i', is_flag=True, help='Display detailed information about scenarios')
def list(scenario, info):
    """List all available scenarios or mark a scenario as completed"""
    if info:
        display_scenario_info()
    elif scenario:
        complete(scenario)
    else:
        list_scenarios()

def complete(scenario):
    """Mark a scenario as completed"""
    if not scenario:
        list_scenarios()
        scenario_number = click.prompt("Enter the number of the scenario you want to mark as completed", type=int)
        if 1 <= scenario_number <= len(SCENARIOS):
            scenario = SCENARIOS[scenario_number - 1].title
        else:
            click.echo("Invalid scenario number.")
            return

    scenario_obj = next((s for s in SCENARIOS if s.title == scenario), None)
    if not scenario_obj:
        click.echo(f"Scenario '{scenario}' not found.")
        return

    mark_scenario_completed(scenario_obj.title)
    click.echo(f"Scenario '{scenario_obj.title}' marked as completed.")

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
@click.option('--info', '-i', is_flag=True, help='Display detailed information about scenarios')
def start_scenario(scenario_name, info):
    """Start a specific scenario"""
    if info:
        display_scenario_info()
        return

    if not scenario_name:
        list_scenarios()
        scenario_number = click.prompt("Enter the number of the scenario you want to start", type=int)
        if 1 <= scenario_number <= len(SCENARIOS):
            scenario_name = SCENARIOS[scenario_number - 1].title
        else:
            click.echo("Invalid scenario number.")
            return

    scenario = next((s for s in SCENARIOS if s.title == scenario_name), None)
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
        scenario.generate_func(REPO_PATH)
    except Exception as e:
        click.echo(f"Error generating scenario: {str(e)}")
        return

    set_current_scenario(scenario_name)

    click.echo(scenario.description)
    click.echo(f"\nYour task: {scenario.task}")
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

    scenario = next((s for s in SCENARIOS if s.title == scenario_name), None)
    if not scenario:
        click.echo(f"Scenario '{scenario_name}' not found.")
        return

    if not os.path.exists(REPO_PATH):
        click.echo("No active scenario found. Please start a scenario first.")
        return

    result = scenario.check_func(REPO_PATH)

    if result:
        click.echo("Congratulations! You've successfully completed the task.")
        mark_scenario_completed(scenario_name)
    else:
        click.echo("Not quite right. Try again or use the 'hint' command for help.")

@cli.command()
@click.argument('scenario_name', required=False)
def hint(scenario_name):
    """Get hints for a specific scenario"""
    if not scenario_name:
        scenario_name = get_current_scenario()
        if not scenario_name:
            click.echo("No active scenario found. Please start a scenario first.")
            return

    scenario = next((s for s in SCENARIOS if s.title == scenario_name), None)
    if not scenario:
        click.echo(f"Scenario '{scenario_name}' not found.")
        return

    hint_index = 0
    while hint_index < len(scenario.hints):
        click.echo(f"Hint {hint_index + 1}: {scenario.hints[hint_index]}")
        if hint_index < len(scenario.hints) - 1:
            choice = click.prompt("Enter 'n' for next hint or 'q' to quit", type=str).lower()
            if choice == 'q':
                break
            elif choice != 'n':
                click.echo("Invalid input. Please enter 'n' or 'q'.")
                continue
        hint_index += 1
    
    if hint_index == len(scenario.hints):
        click.echo("No more hints available.")

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
