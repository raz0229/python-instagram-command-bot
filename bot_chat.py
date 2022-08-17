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
options = Options()
options.binary_location = os.getenv('FIREFOX_EXECUTABLE_PATH')
options.add_argument("--window-size=1920,1080")
options.headless = False

profile = FirefoxProfile(os.getenv('FIREFOX_PROFILE_LOCATION'))

# Download block list to block obscene language and insults
print('[INFO] Downloading blocked keywords list..')
r = requests.get('https://jsonkeeper.com/b/5ULD') 
list = r.json()

blocked_list = list['blocked_list']
blocked_names = list["blocked_names"]
print('[INFO] Blocklist Loaded into bot')

# Configuration
FIRST_NAME = os.getenv("FIRST_NAME")
PATH = os.getenv("GECKODRIVER_PATH")  # path to your downloaded webdriver
driver = webdriver.Firefox(profile, executable_path=PATH, options=options)
print('[INFO] Loading your chats...')
driver.get('https://instagram.com/direct/inbox')
print("[INFO] " + driver.title + " loaded successfully")  # prints title of the webpage

conn_harley = http.client.HTTPSConnection("harley-the-chatbot.p.rapidapi.com")
headers_harley = {
    'content-type': "application/json",
    'Accept': "application/json",
    'X-RapidAPI-Key': os.getenv("HARLEY_CHATBOT_API_KEY"),
    'X-RapidAPI-Host': "harley-the-chatbot.p.rapidapi.com"
    }

conn_aeona = http.client.HTTPSConnection("aeona3.p.rapidapi.com")
headers_aeona = {
    'X-RapidAPI-Key': "85632300dbmsha01f5765f1a7303p18df83jsn83e04aa1780a",
    'X-RapidAPI-Host': "aeona3.p.rapidapi.com"
    }

def deemojify(text):
    return emoji.get_emoji_regexp().sub(r'', text)


def urlify(text, command, target):
    slug = slugify(text.lower().replace(command, '').strip(), separator='%20')
    return f"q={deemojify(slug)}&target={target}"


def load_requests(source_url, sink_path):
    import requests
    r = requests.get(source_url, stream=True)
    if r.status_code == 200:
        with open(sink_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)


def filter_word(word):
    res = [ele for ele in blocked_list if (ele in word)]
    if res:
        return [res]
    #if word in blocked_list:
    #    return [word]
    word = ''.join(sorted(set(word), key=word.index))
    res = [ele for ele in blocked_names if (ele in word)]
    return res


class Bot:
    def __init__(self, contact):
        self.contact = contact
        elem = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, f'//*[text() = "{self.contact}" ]')))
        try:
            notification_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Turn On')]")
            if notification_button:
                notification_button.click()
        except Exception:
            print('[LOG] Could not locate notification button')
        elem.click()
        print("[INFO] Bot running on chat: " + self.contact)
        self.incoming = WebDriverWait(driver, 120).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR ,'._aacl._aaco._aacu._aacx._aad6._aade')))
        self.received_msgs = len(self.incoming)
        self.running = True
        self.pressed_ctrl = False

    def make_call_harley(self, request):
        
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
            self.make_call_harley(request)
        else:  # no error occurred
            return response.replace('Harley', 'RAZBot').replace('robomatic.ai', 'instagram.com/raz0229')  # replace name and location in response


    def make_call_aeona(self, request):
        print("here: call made")
        conn_aeona.request("GET", f"/?text={slugify(request)}&userId=12312312312", headers=headers_aeona)
        
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
        incoming = driver.find_elements(By.CSS_SELECTOR,'._aacl._aaco._aacu._aacx._aad6._aade')
        if len(incoming) != self.received_msgs:
            return True
        else:
            return False

    def send_message(self, text):
        input_box = driver.find_element(By.CSS_SELECTOR,'textarea')
        input_box.click()
        input_box.send_keys(text, Keys.RETURN)
        incoming = driver.find_elements(By.CSS_SELECTOR,'._aacl._aaco._aacu._aacx._aad6._aade')
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
                        self.incoming = driver.find_elements(By.CSS_SELECTOR,'._aacl._aaco._aacu._aacx._aad6._aade')
                        self.received_msgs = len(self.incoming)
                        last_msg = self.incoming[self.received_msgs - 1].text
                        if not last_msg.startswith('💀🦇'):
                            print("[INFO] New message: " + last_msg)
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


