#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Pomodoro  https://en.wikipedia.org/wiki/Pomodoro_Technique
# ====== 🍅 Tomato Clock =======
# ./tomato.py         # start a 25 minutes tomato clock + 5 minutes break
# ./tomato.py -t      # start a 25 minutes tomato clock
# ./tomato.py -t <n>  # start a <n> minutes tomato clock
# ./tomato.py -b      # take a 5 minutes break
# ./tomato.py -b <n>  # take a <n> minutes break
# ./tomato.py -h      # help


import subprocess
import sys
import time
from argparse import ArgumentParser

from plyer import notification

parser = ArgumentParser()
parser.add_argument("-wt", "--work_time", type=int, default=25, help='Number of minutes to work for')
parser.add_argument("-bt", "--break_time", type=int, default=5, help='Number of minutes to rest for')

args = parser.parse_args()


class PlatformNotSupportedException(Exception):
    """
    Raised when the platform is not supported by this script
    """


def main() -> None:
    """
    Main Loop
    """
    while True:
        try:
            print(f'🍅 tomato {args.work_time} minute(s). Ctrl+C to exit')
            tomato(args.work_time, 'Time to take a break!')
            print(f'🛀 break {args.break_time} minute(s). Ctrl+C to exit')
            tomato(args.break_time, 'Time to work!')
        except KeyboardInterrupt:
            print('\n👋 goodbye')
            break


def tomato(minutes: int, notify_msg: str) -> None:
    """
    Handles logic & timing for tomato periods
    :param int minutes: How long this "tomato period" lasts for
    :param str notify_msg: Message to output and notify to the user
    """
    start_time = time.perf_counter()
    while True:
        delta_seconds = int(round(time.perf_counter() - start_time))
        remaining_seconds = minutes * 60 - delta_seconds

        countdown = f'{int(remaining_seconds / 60)}:{int(remaining_seconds % 60):02}'

        if remaining_seconds <= 0:
            print_progress_bar(delta_seconds, minutes * 60, countdown)
            break
        print_progress_bar(delta_seconds, minutes * 60, countdown)
        time.sleep(1)

    notify_me(notify_msg)


def print_progress_bar(current: int, total: int, countdown: str, length: int = 60, fill: str = '█') -> None:
    """
    Handles progress bar logic

    :param int current: current time progress through "tomato period"
    :param int total: total time this "tomato period" lasts
    :param str countdown: current time countdown
    :param int length: length of progress bar fill, defaults to 60
    :param str fill: character to fill the progress bar with, defaults to '█'
    """
    # print('\r', current, total, countdown, '\n')
    percent = f'{(100 * (current / float(total))):.2f}'
    filled_length = int(length * current // total)
    bar_fill = fill * filled_length + '-' * (length - filled_length)
    print(f'\r\t{(countdown)}⏰ |{bar_fill}| {percent}%', end='\r')
    # Print New Line on Complete
    if current == total:
        print()


def notify_me(msg: str):
    '''
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -> message <msg>

    # ubuntu desktop notification
    notify-send

    # voice notification
    say -v <lang> <msg>
    lang options:
    - Daniel:       British English
    - Ting-Ting:    Mandarin
    - Sin-ji:       Cantonese
    '''

    print(msg)
    if sys.platform == 'darwin':
        # macos desktop notification
        subprocess.run(['terminal-notifier', '-title', '🍅', '-message', msg])
        subprocess.run(['say', '-v', 'Daniel', msg])
    elif sys.platform.startswith('linux'):
        # ubuntu desktop notification
        subprocess.Popen(["notify-send", '🍅', msg])
    elif sys.platform == 'win32':
        if "work" in msg:
            title = 'Work!'
        else:
            title = 'Break!'
        notification.notify(    # type: ignore
            title=title,
            message=msg,
            timeout=10,
            app_icon='tomato.ico'
        )
    else:
        raise PlatformNotSupportedException(
            f'The following platform is not yet supported by this script: {sys.platform}')


if __name__ == "__main__":
    main()
