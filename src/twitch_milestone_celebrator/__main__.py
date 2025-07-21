"""Main entry point for the Twitch Milestone Celebrator."""
import sys

from twitch_milestone_celebrator.bot.twitch_bot import run_bot


def main() -> None:
    """Run the Twitch Milestone Celebrator."""
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
