# see 'main.py'
import os

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium import webdriver
from pynput import keyboard
from slugify import slugify
from fancy import Fancy
import pyautogui as gui
from animu import client as acl
import http.client
import wikipedia
import asyncio
import requests
import socket
import emoji
import json
import gc
import os
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

waifu = acl.Client("eae6c4c7e1a3fffe31e383371dd477d82649ac579117")
profile = FirefoxProfile("/home/raz0229/.mozilla/firefox/58m1hr3k.dev-edition-default")
# Configuration
PATH = "/home/raz0229/Downloads/geckodriver"  # path to your downloaded webdriver
driver = webdriver.Firefox(profile, executable_path=PATH, options=options)
driver.get('https://instagram.com/direct/inbox')
print(driver.title)  # prints title of the webpage

conn = http.client.HTTPSConnection("robomatic-ai.p.rapidapi.com", timeout=10)
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'X-RapidAPI-Host': "robomatic-ai.p.rapidapi.com",
    'X-RapidAPI-Key': "85632300dbmsha01f5765f1a7303p18df83jsn83e04aa1780a"
    }

connTranslate = http.client.HTTPSConnection("google-translate1.p.rapidapi.com")
headersTranslate = {
    'content-type': "application/x-www-form-urlencoded",
    'Accept-Encoding': "application/gzip",
    'X-RapidAPI-Host': "google-translate1.p.rapidapi.com",
    'X-RapidAPI-Key': "85632300dbmsha01f5765f1a7303p18df83jsn83e04aa1780a"
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
            print(response)
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
        input_box.send_keys(text, Keys.RETURN)
        incoming = driver.find_elements_by_css_selector('._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll')
        self.received_msgs = len(incoming)

    def send_copied_image(self):
        input_box = driver.find_element_by_css_selector('textarea')
        input_box.click()
        input_box.send_keys(Keys.LEFT_CONTROL, "v")
        send_button = driver.find_element_by_css_selector(".sqdOP.L3NKy._4pI4F.y3zKF.cB_4K")
        send_button.click()
        incoming = driver.find_elements_by_css_selector('._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll')
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
            if self.new_msg_received():

                    self.incoming = driver.find_elements_by_css_selector('._7UhW9.xLCgt.MMzan.KV-D4.uL8Hv.T0kll')
                    self.received_msgs = len(self.incoming)
                    last_msg = self.incoming[self.received_msgs - 1].text
                    print(last_msg)

                    # BOT response
                    if last_msg.lower().startswith("bot_ask"):
                        self.send_message('Thinking... 🤖🦇')

                        if deemojify(last_msg.lower().strip()) == "bot_ask":
                            self.send_message("🤖🦇 Chat with me using bot_ask command. Example: bot_ask who are you")
                        else:
                            self.send_message(self.make_call(deemojify(last_msg.replace("bot_ask", '').strip())))

                    # Translate to Pashto
                    elif last_msg.lower().startswith("bot_pashto"):
                        payloadPashto = urlify(last_msg, "bot_pashto", "ps")
                        self.send_message("🤖🦇 Translating last message to Pashto...")
                        try:
                            connTranslate.request("POST", "/language/translate/v2", payloadPashto, headersTranslate)
                            resPashto = connTranslate.getresponse()
                            dataPashto = resPashto.read()
                        except http.client.HTTPException:
                            self.send_message("🤖🦇 Error translating. Try again")
                        else:
                            self.send_message(json.loads(dataPashto.decode("utf-8"))["data"]["translations"][0]['translatedText'])

                    # Translate to English
                    elif last_msg.lower().startswith("bot_english"):
                        payloadEng = urlify(last_msg, "bot_english", "en")
                        self.send_message("🤖🦇 Translating last message to English...")
                        try:
                            connTranslate.request("POST", "/language/translate/v2", payloadEng, headersTranslate)
                            resEng = connTranslate.getresponse()
                            dataEng = resEng.read()
                        except http.client.HTTPException:
                            self.send_message("🤖🦇 Error translating. Try again")
                        else:
                            self.send_message(json.loads(dataEng.decode("utf-8"))["data"]["translations"][0]['translatedText'])

                    # Translate to Urdu
                    elif last_msg.lower().startswith("bot_urdu"):
                        payloadUr = urlify(last_msg, "bot_urdu", "ur")
                        self.send_message("🤖🦇 Translating last message to Urdu...")
                        try:
                            connTranslate.request("POST", "/language/translate/v2", payloadUr, headersTranslate)
                            resUr = connTranslate.getresponse()
                            dataUr = resUr.read()
                        except http.client.HTTPException:
                            self.send_message("🤖🦇 Error translating. Try again")
                        else:
                            print(json.loads(dataUr.decode("utf-8"))["data"])
                            self.send_message(json.loads(dataUr.decode("utf-8"))["data"]["translations"][0]['translatedText'])

                    # Search Wikipedia
                    elif last_msg.lower().startswith("bot_wiki"):
                        msg = deemojify(last_msg.lower().replace("bot_wiki", "").strip())
                        self.send_message(f"🤖🦇 Searching Wikipedia for: {msg}")
                        try:
                            response = wikipedia.summary(msg, auto_suggest=False)
                        except Exception as wk:
                            self.send_message(str(wk))
                        else:
                            self.send_message(response)

                    # Fancy text converter
                    elif last_msg.lower().startswith("bot_fancy"):
                        text = deemojify(last_msg.lower().replace("bot_fancy", "").strip())
                        fn = Fancy(text)
                        for i in range(25):
                            self.send_message(fn.makeFancy(i+1))

                    # Anime quote
                    elif last_msg.lower().startswith("bot_quote"):
                        try:
                            quote = asyncio.run(waifu.quote())
                            self.send_message(quote["quote"])
                        except Exception:
                            self.send_message("🤖🦇 Cannot get Quote due to slow internet")

                    # Fetch waifu
                    elif last_msg.lower().startswith("bot_waifu"):
                        self.send_message("🤖🦇 Fetching a hot waifu. This could take a while...")
                        try:
                            waf = asyncio.run(waifu.waifu())
                            load_requests(waf["images"][0], "waifu.png")
                            os.system("xclip -selection clipboard -t image/png -i ~/Documents/python-instagram-command-bot/waifu.png")
                            self.send_copied_image()
                        except Exception:
                            self.send_message("🤖🦇 Slow internet while fetching waifu")

                    else:
                        print("No command")
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
