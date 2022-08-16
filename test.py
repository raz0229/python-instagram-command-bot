import signal
import sys

def sigint_handler(signal, frame):
    print('KeyboardInterrupt is caught')
    sys.exit(0)

while True:
    signal.signal(signal.SIGINT, sigint_handler)
