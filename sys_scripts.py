#   References:
#
#   https://stackoverflow.com/questions/9246076/how-to-print-one-character-at-a-time-on-one-line
#

import time
import sys

# prints out text slowly
# purely for user interaction


def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.03)
