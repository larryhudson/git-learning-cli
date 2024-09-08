# cli.py

import click
import os
import shutil
from scenario import scenarios

REPO_PATH = os.path.join(os.getcwd(), "learning_repo")

@click.group()
def cli():
    """Git Learning CLI"""
    pass

@cli.command()
def list_scenarios():
    """List all available scenarios"""
    click.echo("Available scenarios:")
    for idx, scenario in enumerate(scenarios, 1):
        click.echo(f"{idx}. {scenario['title']}")

@cli.command()
@click.argument('scenario_name')
def start_scenario(scenario_name):
    """Start a specific scenario"""
    scenario = next((s for s in scenarios if s['title'] == scenario_name), None)
    if not scenario:
        click.echo(f"Scenario '{scenario_name}' not found.")
        return

    if 'generator' not in scenario:
        click.echo(f"Error: The scenario '{scenario_name}' is not properly configured (missing 'generator').")
        return

    if os.path.exists(REPO_PATH):
        shutil.rmtree(REPO_PATH)
    os.mkdir(REPO_PATH)

    try:
        scenario_info = scenario['generator'](REPO_PATH)
    except Exception as e:
        click.echo(f"Error generating scenario: {str(e)}")
        return

    if not isinstance(scenario_info, dict) or 'description' not in scenario_info or 'task' not in scenario_info:
        click.echo("Error: The scenario generator didn't return the expected information.")
        return

    click.echo(scenario_info['description'])
    click.echo(f"\nYour task: {scenario_info['task']}")
    click.echo(f"\nThe Git repository has been set up at: {REPO_PATH}")
    click.echo("Once you've completed the task, use the 'check' command to verify your solution.")

@cli.command()
@click.argument('scenario_name')
def check(scenario_name):
    """Check the solution for a specific scenario"""
    scenario = next((s for s in scenarios if s['title'] == scenario_name), None)
    if not scenario:
        click.echo(f"Scenario '{scenario_name}' not found.")
        return

    if not os.path.exists(REPO_PATH):
        click.echo("No active scenario found. Please start a scenario first.")
        return

    scenario_info = scenario['generator'](REPO_PATH)
    result = scenario_info['check_function'](REPO_PATH)

    if result:
        click.echo("Congratulations! You've successfully completed the task.")
    else:
        click.echo("Not quite right. Try again or use the 'hint' command for help.")

@cli.command()
@click.argument('scenario_name')
def hint(scenario_name):
    """Get a hint for a specific scenario"""
    scenario = next((s for s in scenarios if s['title'] == scenario_name), None)
    if not scenario:
        click.echo(f"Scenario '{scenario_name}' not found.")
        return

    if 'hint' in scenario:
        click.echo(scenario['hint'])
    else:
        click.echo("Hint: Review the Git commands related to this scenario and think about the steps needed to accomplish the task.")

@cli.command()
def reset():
    """Reset the current scenario"""
    if os.path.exists(REPO_PATH):
        shutil.rmtree(REPO_PATH)
        click.echo("The current scenario has been reset. Use the 'start_scenario' command to begin again.")
    else:
        click.echo("No active scenario found. Use the 'start_scenario' command to begin a new scenario.")

if __name__ == '__main__':
    cli()
