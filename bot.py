# see 'main.py'

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from pynput import keyboard
from slugify import slugify
import pyautogui as gui
import http.client
import socket
import emoji
import json
import gc

options = Options()
options.add_argument("user-data-dir=/tmp/raz0229")
# Configuration
PATH = "/opt/chromedriver"  # path to your downloaded webdriver
driver = webdriver.Chrome(PATH, chrome_options=options)
driver.get('https://instagram.com/direct/inbox')
print(driver.title)  # prints title of the webpage

conn = http.client.HTTPSConnection("robomatic-ai.p.rapidapi.com", timeout=10)
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'X-RapidAPI-Host': "robomatic-ai.p.rapidapi.com",
    'X-RapidAPI-Key': "85632300dbmsha01f5765f1a7303p18df83jsn83e04aa1780a"
    }


def deemojify(text):
    return emoji.get_emoji_regexp().sub(r'', text)


class Bot:
    def __init__(self, contact):
        self.contact = contact
        elem = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, f'//*[text() = "{self.contact}" ]')))
        elem.click()
        self.incoming = WebDriverWait(driver, 120).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR ,'._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll')))
        self.received_msgs = len(self.incoming)
        self.running = True
        self.pressed_ctrl = False

    def make_call(self, request):
        request = slugify(request, separator='%20')
        payload = f"in={request}&op=in&cbot=1&SessionID=RapidAPI1&ChatSource=RapidAPI&cbid=1&key=RHMN5hnQ4wTYZBGCF3dfxzypt68rVP"
        response = " "
        try:
            conn.request("POST", "/api.php", payload, headers)
            res = conn.getresponse()
            data = res.read()
            response = json.loads(data.decode("utf-8"))["out"]
        except socket.timeout:
            return "ERR: Slow Internet connect on host"
        except http.client.HTTPException:
            return "Something went wrong. Try again"
        else:  # no error occurred
            return response.replace('RoboMatic', 'RAZBot').replace('robomatic.ai', 'instagram.com/raz0229')  # replace name and location in response

    def new_msg_received(self):
        incoming = driver.find_elements_by_css_selector('._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll')
        if len(incoming) != self.received_msgs:
            return True
        else:
            return False

    def send_message(self, text):
        input_box = driver.find_element_by_css_selector('textarea')
        input_box.click()
        input_box.send_keys(deemojify(text), Keys.RETURN)
        incoming = driver.find_elements_by_css_selector('._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll')
        self.received_msgs = len(incoming)

    def on_press(self, key):
        print(key, 'Key pressed')
        if key == keyboard.Key.ctrl_l:  # If 'Left Ctrl' is the key pressed
            try:
                self.pressed_ctrl = True
            except Exception as e:
                print(f'{self.contact}: No such contact')
                print(e)
                pass

    def init_bot(self):
        while self.running:
            if self.new_msg_received():
                try:
                    self.incoming = driver.find_elements_by_css_selector('._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll')
                    self.received_msgs = len(self.incoming)
                    last_msg = self.incoming[self.received_msgs - 1].text
                    print(last_msg)

                    # BOT response
                    if last_msg.lower().startswith("bot_ask"):
                        self.send_message('Thinking...')

                        if deemojify(last_msg.lower().strip()) == "bot_ask":
                            self.send_message("Chat with me using bot_ask command. Example: bot_ask who are you")
                        else:
                            self.send_message(self.make_call(last_msg.replace("bot.ask", '').strip()))
                except Exception as e:
                    summary = str(e)
                    self.send_message(summary)
                    print(e)
                    pass
            if self.pressed_ctrl:
                break
        self.contact = gui.prompt('Enter contact\'s name', 'WhatsApp Chat bot')
        print(self.contact, type(self.contact))
        driver.find_element_by_xpath(f'//*[text() = "{self.contact}" ]').click()
        self.pressed_ctrl = False
        self.init_bot()

    # In case you have to stop the program for some reason
    def stop_bot(self):
        self.running = False
        print('Bot stopped')
        gc.collect()
