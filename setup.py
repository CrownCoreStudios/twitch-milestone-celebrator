"""Setup script for Twitch Milestone Celebrator."""

from pathlib import Path

from setuptools import setup

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# This setup.py is kept for backward compatibility and editable installs
# The main configuration is in pyproject.toml
setup(
    name="twitch-milestone-celebrator",
    version="0.1.0",
    author="CrownCore Studios",
    author_email="crowncorestudios@gmail.com",
    description="A Twitch bot that celebrates chat milestones with visual and audio effects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrownCoreStudios/twitch-milestone-celebrator",
    project_urls={
        "Bug Tracker": "https://github.com/CrownCoreStudios/twitch-milestone-celebrator/issues",
        "Source": "https://github.com/CrownCoreStudios/twitch-milestone-celebrator",
    },
    packages=["twitch_milestone_celebrator"],
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.5.2",
        "twitchio>=2.10.0",
        "python-dotenv>=1.0.0",
        "gtts>=2.5.1",
        "requests>=2.31.0",
        "pygame-gui>=0.6.9",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.0.0",
            "black>=23.3.0",
            "isort>=5.12.0",
            "mypy>=1.3.0",
            "flake8>=6.0.0",
            "pre-commit>=3.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "twitch-milestone-celebrator=twitch_milestone_celebrator.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "twitch_milestone_celebrator": ["py.typed", "*.ttf", "*.png", "*.mp3"],
    },
    # Metadata
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Games/Entertainment",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Communications :: Chat",
    ],
)
