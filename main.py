from pynput import keyboard
from bot import Bot as Bot_Std
from bot_chat import Bot as Bot_Chat
import sys
import argparse 
 
# Initialize parser
parser = argparse.ArgumentParser()
 
# Adding optional argument
parser.add_argument("-c", "--chat", required=True)
parser.add_argument("-H", "--headless")
parser.add_argument("-C", "--chatmode")
 
# Read arguments from command line
args = parser.parse_args()

if len(sys.argv) <= 1:
    print('Not enough arhuments')
    with open('usage.txt', 'r') as f:
        print(f.read())
    sys.exit(1)
else:
    headless = True if args.headless == 'True' or args.headless == 'true' else False
    if args.chatmode:
        if args.chatmode.lower() == "male":
            my_bot = Bot_Chat(args.chat, HEADLESS=headless, BOT="male")
        else:
            my_bot = Bot_Chat(args.chat, HEADLESS=headless, BOT="female")
    else:
        my_bot = Bot_Std(args.chat, HEADLESS=headless)

# Keyboard event listener
listener = keyboard.Listener(on_press=my_bot.on_press)
listener.start()

my_bot.init_bot()
