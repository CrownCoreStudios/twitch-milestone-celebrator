# Contributing to Twitch Milestone Celebrator

Thank you for your interest in contributing to Twitch Milestone Celebrator! We appreciate your time and effort to help improve this project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/CrownCoreStudios/twitch-milestone-celebrator.git
   cd twitch-milestone-celebrator
   ```
3. **Set up the development environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   pre-commit install
   ```

## 🔧 Development Workflow

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-number-description
   ```

2. **Make your changes** and ensure they follow our code style:
   - Run `black .` to format your code
   - Run `isort .` to sort imports
   - Run `mypy src/` to check types
   - Run `flake8` to check for style issues

3. **Write tests** for your changes (if applicable)

4. **Run the tests** to make sure everything works:
   ```bash
   pytest
   ```

5. **Commit your changes** with a descriptive message:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

6. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

7. **Open a Pull Request** against the `main` branch

## 📝 Pull Request Guidelines

- Keep PRs focused on a single feature or bugfix
- Write clear, concise commit messages
- Update the documentation if necessary
- Include tests for new features
- Ensure all tests pass
- Reference any related issues in your PR description

## 🐛 Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Environment information (OS, Python version, etc.)
- Any relevant error messages or screenshots

## 💡 Feature Requests

We welcome feature requests! Please open an issue with:
- A clear description of the feature
- The problem it solves
- Any alternative solutions you've considered

## 📚 Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use type hints for all function signatures
- Write docstrings for all public functions and classes
- Keep lines under 88 characters (Black's default)

## 📜 License

By contributing to this project, you agree that your contributions will be licensed under the [CrownCore Studios License](LICENSE).

---

Thank you for helping make Twitch Milestone Celebrator better! 🎉
