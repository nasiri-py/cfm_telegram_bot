import argparse


parser = argparse.ArgumentParser(description="Run telegram bot")

parser.add_argument("command", choices=['runtel'])

args = parser.parse_args()

if args.command == 'runtel':
    from bot import bot_runner
    bot_runner()
