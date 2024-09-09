# Git Learning CLI

This Git Learning CLI is an interactive tool designed to help you improve your Git skills through hands-on scenarios. It provides a series of practical exercises that simulate real-world Git situations, allowing you to practice and master various Git commands and workflows.

## Features

- Multiple scenarios with varying difficulty levels (Easy, Medium, Hard)
- Interactive CLI interface
- Scenario generation and validation
- Progress tracking
- Hint system for each scenario

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/larryhudson/git-learning-cli.git
   cd git-learning-cli
   ```

2. Install the CLI:
   ```
   pip install .
   ```

## Usage

After installation, you can use the `git-learn` command to interact with the Git Learning CLI. Here are the available subcommands:

- `list`: Display all available scenarios
- `start-scenario`: Start a specific scenario
- `check`: Check your solution for the current scenario
- `hint`: Get hints for the current scenario
- `complete`: Mark a scenario as completed
- `reset`: Reset the current scenario

### Getting Started

1. List all available scenarios:
   ```
   git-learn list
   ```

2. Start a scenario:
   ```
   git-learn start-scenario
   ```
   You'll be prompted to choose a scenario if you don't specify one.

3. Work on the scenario in the generated Git repository (located in your home directory).

4. Check your solution:
   ```
   git-learn check
   ```

5. If you need help, use the hint system:
   ```
   git-learn hint
   ```

6. Once you've completed a scenario, you can mark it as completed:
   ```
   git-learn complete
   ```

7. To start over, reset the current scenario:
   ```
   git-learn reset
   ```

## Scenarios

The Git Learning CLI includes various scenarios covering different Git concepts and workflows:

1. Stash Changes and Apply (Easy)
2. Create and Apply a Patch (Medium)
3. Squash Commits (Medium)
4. Recover from Detached HEAD State (Medium)
5. Cherry-pick a Commit (Medium)
6. Split a Large Commit (Hard)
7. Split Commit to Multiple Branches (Hard)
8. Find a Bug with Git Bisect (Hard)
9. Resolve Binary File Merge Conflict (Hard)

Each scenario provides a unique challenge to help you practice specific Git skills.

## Contributing

If you'd like to contribute to this project by adding new scenarios or improving existing ones, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature
3. Implement your changes
4. Submit a pull request

Please ensure that any new scenarios follow the existing format and include appropriate difficulty levels, descriptions, tasks, and hint systems.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
