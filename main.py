# https://github.com/raz0229/python-whatsapp-chatbot.git
#
# Simple python-whatsapp bot built with selenium webdriver and PyAutoGUI hooked with
# 3rd-party Acobot API to respond to your requests.
# Webdriver configuration and your private API key found in 'bot.py' file and can be changed accordingly
#
# External packages you might need to install:
# pip install selenium pynput pyautogui
#
# Required Webdriver for your version of Google Chrome can be downloaded from
# https://sites.google.com/a/chromium.org/chromedriver/downloads
#
# Acobot (Chat bot) API endpoint and documentation can be found at
# https://rapidapi.com/Acobot/api/brainshop-ai/
#
# Created instance 'my_bot' of class Bot takes in a 'contact' as argument which is merely the contact
# in your WhatsApp chat panel to target. Although it is required initially, it can be changed later
# through the GUI prompt by pressing the 'Left Ctrl' key on your keyboard.
#
# Keyboard.listener object in main.py creates a new non-blocking thread and listens to the key pressed
# event with keyboard.Key.ctrl_l (Left Ctrl key) as main key to show the 'Change contact' prompt.
# This main key can be changed on line 64 of 'bot.py' with another key or key combination for which you
# may refer to the official pynput documentation.

from pynput import keyboard
from bot import Bot

my_bot = Bot('Sovereign Queendom of Hunsville') #Haram Chads🔥❤

# Keyboard event listener
listener = keyboard.Listener(on_press=my_bot.on_press)
listener.start()

my_bot.init_bot()
