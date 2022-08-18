from urllib import response
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium import webdriver
from pynput import keyboard
from slugify import slugify
import pyautogui as gui
from random import randint
import http.client
import asyncio
import requests
import socket
import random
import emoji
import signal
import json
import gc
from dotenv import load_dotenv
import os
from selenium.webdriver.firefox.options import Options

load_dotenv()

conn_harley = http.client.HTTPSConnection("harley-the-chatbot.p.rapidapi.com")
headers_harley = {
    'content-type': "application/json",
    'Accept': "application/json",
    'X-RapidAPI-Key': os.getenv("X_RAPIDAPI_KEY"),
    'X-RapidAPI-Host': "harley-the-chatbot.p.rapidapi.com"
    }

conn_aeona = http.client.HTTPSConnection("aeona3.p.rapidapi.com")
headers_aeona = {
    'X-RapidAPI-Key': os.getenv("X_RAPIDAPI_KEY"),
    'X-RapidAPI-Host': "aeona3.p.rapidapi.com"
    }

def deemojify(text):
    return emoji.get_emoji_regexp().sub(r'', text)


class Bot:
    
    def __init__(self, contact, HEADLESS=False, BOT="female"):

        self.contact = contact
        self.HEADLESS = HEADLESS
        self.BOT = BOT
        
        options = Options()
        options.binary_location = os.getenv('FIREFOX_EXECUTABLE_PATH')
        options.add_argument("--window-size=1920,1080")
        options.headless = self.HEADLESS

        profile = FirefoxProfile(os.getenv('FIREFOX_PROFILE_LOCATION'))

        PATH = os.getenv("GECKODRIVER_PATH")  # path to your downloaded webdriver
        self.driver = webdriver.Firefox(profile, executable_path=PATH, options=options)
        if self.BOT.lower() == "female":
            print('[INFO] Chat Mode: Aeona (Female)')
        else:
            print('[INFO] Chat Mode: Harley (Male)')
        print('[INFO] Loading your chats...')
        self.driver.get('https://instagram.com/direct/inbox')
        # prints title of the webpage
        print("[INFO] " + self.driver.title + " loaded successfully")

        elem = WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, f'//*[text() = "{self.contact}" ]')))
        try:
            notification_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Turn On')]")
            if notification_button:
                notification_button.click()
        except Exception:
            print('[LOG] Could not locate notification button')
        elem.click()
        print("[INFO] Bot running on chat: " + self.contact + " in Chat Mode")
        self.incoming = WebDriverWait(self.driver, 120).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR ,'._aacl._aaco._aacu._aacx._aad6._aade')))
        self.received_msgs = len(self.incoming)
        self.running = True
        self.pressed_ctrl = False

    def make_call_harley(self, request):
        
        url = "https://harley-the-chatbot.p.rapidapi.com/talk/bot"
        payload = {
	        "client": "",
	        "bot": "harley",
	        "message": request
        }

        try:
            conn_harley.request("POST", "/talk/bot", json.dumps(payload), headers_harley)
            res = conn_harley.getresponse()
            data = res.read()
            response = json.loads(data.decode("utf-8"))['data']['conversation']['output']
        except socket.timeout:
            return "ERR: Slow Internet connect on host"
        except http.client.HTTPException:
            print('http exception')
            self.make_call_harley(request)
        else:  # no error occurred
            return response.replace('Harley', 'RAZBot').replace('robomatic.ai', 'instagram.com/raz0229')  # replace name and location in response


    def make_call_aeona(self, request):
        conn_aeona.request("GET", f"/?text={slugify(request)}&userId={ os.getenv('AEONA_USER_ID') }", headers=headers_aeona)
        
        try:
            res = conn_aeona.getresponse()
            data = res.read()
            response = data.decode("utf-8")
        except socket.timeout:
            return "ERR: Slow Internet connect on host"
        except http.client.HTTPException:
            self.make_call(request)
        else:  # no error occurred
            return response.replace('Aeona', 'RAZBot').replace('Oakland, California', 'RazRiG').replace("dash", "-")  # replace name and location in response


    def new_msg_received(self):
        incoming = self.driver.find_elements(By.CSS_SELECTOR,'._aacl._aaco._aacu._aacx._aad6._aade')
        if len(incoming) != self.received_msgs:
            return True
        else:
            return False

    def send_message(self, text):
        input_box = self.driver.find_element(By.CSS_SELECTOR,'textarea')
        input_box.click()
        input_box.send_keys(text, Keys.RETURN)
        incoming = self.driver.find_elements(By.CSS_SELECTOR,'._aacl._aaco._aacu._aacx._aad6._aade')
        self.received_msgs = len(incoming)

    def on_press(self, key):
        print(key, 'Key pressed')
        if key == keyboard.Key.ctrl_r:  # If 'Left Ctrl' is the key pressed
            try:
                self.pressed_ctrl = True
            except Exception as e:
                print(f'{self.contact}: No such contact')
                print(e)
                pass

    def init_bot(self):
        while self.running:
            signal.signal(signal.SIGINT, self.stop_bot)
            if self.new_msg_received():

                    try:
                        self.incoming = self.driver.find_elements(By.CSS_SELECTOR,'._aacl._aaco._aacu._aacx._aad6._aade')
                        self.received_msgs = len(self.incoming)
                        last_msg = self.incoming[self.received_msgs - 1].text
                        if not last_msg.startswith('💀🦇'):
                            print("[INFO] New message: " + last_msg)
                            if self.BOT.lower() == "male":
                               self.send_message('💀🦇 ' + self.make_call_harley(deemojify(last_msg.strip())))
                            else:
                                self.send_message('💀🦇 ' + self.make_call_aeona(deemojify(last_msg.strip())))

                    except Exception:
                        last_msg = 'Something exception'

            if self.pressed_ctrl:
                break
        self.contact = gui.prompt('Enter contact\'s name', 'Instagram command bot')
        print(self.contact, type(self.contact))
        driver.find_element(By.XPATH, f'//*[text() = "{self.contact}" ]').click()
        self.pressed_ctrl = False
        self.init_bot()

    # In case you have to stop the program for some reason
    def stop_bot(self, signal, frame):
        self.send_message("[🤖🦇] Service RazBot v4.0 (main.py) terminated by the administrator")
        time.sleep(3)
        self.running = False
        print('Bot stopped')
        gc.collect()

def sigint_handler(signal, frame):
    print ('KeyboardInterrupt is caught')
    my_bot.stop_bot()
    sys.exit(0)


