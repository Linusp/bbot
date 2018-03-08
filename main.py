from __future__ import unicode_literals, print_function

import sys
import argparse

from bearybot.bot import BearyBot
from bearybot.controller import Controller


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a BearyBot')
    parser.add_argument('-w', '--word', type=str,
                        help='Set trigger word of bot.')
    parser.add_argument('-p', '--port', type=int,
                        help='Set port the bot listen, default value is 7428')

    args = parser.parse_args()

    trigger_word = args.word
    port = args.port
    if not trigger_word:
        print('no trigger word is given!.')
        sys.exit(1)
    if port is None:
        print('no port is given!.')
        sys.exit(1)

    controller = Controller()
    bot = BearyBot(trigger_word, controller)

    bot.run(port=port)
