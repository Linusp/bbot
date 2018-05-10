from __future__ import unicode_literals, print_function

import argparse

from .bot import BearyBot
from .controller import Controller


def main():
    parser = argparse.ArgumentParser(description='Start a BearyBot')
    parser.add_argument('-w', '--word', type=str, required=True,
                        help='Set trigger word of bot.')
    parser.add_argument('-p', '--port', type=int, required=True,
                        help='Set port the bot listen, default value is 7428')

    args = parser.parse_args()

    trigger_word = args.word
    port = args.port

    controller = Controller()
    bot = BearyBot(trigger_word, controller)

    bot.run(port=port)


if __name__ == '__main__':
    main()
