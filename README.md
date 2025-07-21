# Twitch Milestone Celebrator

<p align="center">
  <img src="https://github.com/CrownCoreStudios/.github/raw/main/profile/crowncore-logo.png" alt="CrownCore Studios Logo" width="200"/>
</p>

> A Twitch bot that celebrates chat milestones with visual and audio effects

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A sophisticated Python application that celebrates Twitch chat milestones and events with customizable visual and audio effects. The application runs as a Twitch chat bot that can detect keywords, follower events, and viewer milestones, triggering beautiful on-screen celebrations.

## ✨ Features

- 🎉 Monitors Twitch chat for keywords and viewer milestones
- 🔊 Plays celebration sound effects when milestones are reached
- 🎨 Displays beautiful visual effects on screen when triggered
- ⚙️ Configurable through environment variables
- 🗣️ Text-to-speech announcements for milestones
- 🚀 Easy to set up and customize
- 🏆 Proudly developed by CrownCore Studios

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- A Twitch account with [developer access](https://dev.twitch.tv/console)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/CrownCoreStudios/twitch-milestone-celebrator.git
   cd twitch-milestone-celebrator
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package**
   ```bash
   pip install -e .
   ```

4. **Configure your environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Twitch credentials
   ```

5. **Run the bot**
   ```bash
   python -m twitch_milestone_celebrator
   ```

## ⚙️ Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `TWITCH_BOT_USERNAME` | Your Twitch bot's username | `mybot` |
| `TWITCH_OAUTH_TOKEN` | OAuth token for the bot | `oauth:xxxxxxxxxxxxxxxx` |
| `TWITCH_CHANNEL` | Channel to monitor | `mychannel` |
| `TWITCH_CLIENT_ID` | Twitch API client ID | `xxxxxxxxxxxxxxxxxxxxxxxxxx` |
| `TWITCH_CLIENT_SECRET` | Twitch API client secret | `xxxxxxxxxxxxxxxxxxxxxxxxxx` |

### Optional Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `TTS_ENABLED` | `true` | Enable/disable text-to-speech |
| `TTS_LANGUAGE` | `en` | Language for TTS (e.g., 'en', 'es') |
| `VIEWER_MILESTONES` | `1,5,10,25,50,100` | Comma-separated viewer counts to celebrate |
| `CHAT_KEYWORDS` | `poggers,lets go,gg` | Comma-separated keywords that trigger celebrations |
| `BOT_OWNER` | - | Username of the bot owner (for admin commands) |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |

### Getting Twitch Credentials
1. Go to [Twitch Developer Console](https://dev.twitch.tv/console)
2. Register a new application
3. Get your Client ID and Client Secret
4. Generate an OAuth token at [Twitch Token Generator](https://twitchtokengenerator.com/) with `chat:read` and `chat:edit` scopes

### Customizing Celebrations

You can customize the celebrations by modifying the `UIConfig` class in `src/twitch_milestone_celebrator/config/settings.py`. Available options include:

- Window size and position
- Colors and fonts
- Animation durations
- Emoji and particle effects

## 🎮 Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `!celebrate [message]` | Trigger a celebration | Moderators |
| `!addkeyword [keyword]` | Add a new trigger keyword | Moderators |
| `!listkeywords` | List all trigger keywords | Everyone |

## 🛠 Development

### Setting Up for Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/CrownCoreStudios/twitch-milestone-celebrator.git
   cd twitch-milestone-celebrator
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   pre-commit install
   ```

### Running Tests

```bash
pytest
```

### Code Style

We use:
- [Black](https://github.com/psf/black) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [mypy](http://mypy-lang.org/) for static type checking

```bash
black .
isort .
mypy src/
```

## 📁 Project Structure

```
twitch-milestone-celebrator/
├── .github/              # GitHub workflows and templates
├── src/
│   └── twitch_milestone_celebrator/
│       ├── bot/           # Twitch bot implementation
│       ├── ui/            # Pygame window and visual effects
│       ├── config/        # Configuration management
│       ├── utils/         # Utility functions
│       └── effects/       # Visual and audio effects
├── tests/                # Test files
├── .env.example          # Example environment variables
├── pyproject.toml        # Project metadata and dependencies
├── setup.py             # Package installation script
└── README.md            # This file
```

# With pip
pytest
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [TwitchIO](https://github.com/TwitchIO/TwitchIO)
- Visual effects powered by [Pygame](https://www.pygame.org/)
- Text-to-speech by [gTTS](https://gtts.readthedocs.io/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👥 Contributors

- [CrownCore Studios](https://github.com/CrownCoreStudios)

## 📧 Contact

CrownCore Studios - [@CrownCoreStudio](https://x.com/CrownCoreStudio)
