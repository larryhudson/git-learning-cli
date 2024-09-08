# cli.py

import click
import os
import shutil
from pathlib import Path
from scenario import scenarios

HOME_DIR = str(Path.home())
REPO_PATH = os.path.join(HOME_DIR, "git_learning_repo")

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

    if os.path.exists(REPO_PATH):
        shutil.rmtree(REPO_PATH)
    os.mkdir(REPO_PATH)

    # Initialize Git repository
    try:
        import git
        git.Repo.init(REPO_PATH)
    except ImportError:
        click.echo("GitPython is not installed. Please install it using 'pip install GitPython'")
        return
    except Exception as e:
        click.echo(f"Error initializing Git repository: {str(e)}")
        return

    try:
        scenario['generate_func'](REPO_PATH)
    except Exception as e:
        click.echo(f"Error generating scenario: {str(e)}")
        return

    click.echo(scenario['description'])
    click.echo(f"\nYour task: {scenario['task']}")
    click.echo(f"\nThe Git repository has been set up at: {REPO_PATH}")
    click.echo("This is a separate directory in your home folder to avoid conflicts with existing repositories.")
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

    result = scenario['check_func'](REPO_PATH)

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

    click.echo(scenario['hint'])

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
