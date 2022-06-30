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
from random import randint
import http.client
import wikipedia
import asyncio
import requests
import socket
import emoji
import random
import json
import gc
import os
from selenium.webdriver.firefox.options import Options
from apiclient.discovery import build
from youtubesearchpython import VideosSearch

options = Options()
options.headless = False

waifu = acl.Client("eae6c4c7e1a3fffe31e383371dd477d82649ac579117")
profile = FirefoxProfile("/home/raz0229/.mozilla/firefox/58m1hr3k.dev-edition-default")

blocked_list = ["mom", "dad", "mother", "father", "mommy", "moma", "mama", "sister", "sissy",  "lu", "phudi", "phodi", "chut", "bund", "bond", "fuck", "gashti", "pencho"]
blocked_names = ["talh", "batol", "raz", "abdulh", "wahb", "janua", "jinua", "raj", "zafr", "janu", "nor", "tlha", "btol", "mustaf", "ali", "chris", "an"]

# Configuration
PATH = "/home/raz0229/Downloads/geckodriver"  # path to your downloaded webdriver
driver = webdriver.Firefox(profile, executable_path=PATH, options=options)
driver.get('https://instagram.com/direct/inbox')
print(driver.title)  # prints title of the webpage

conn = http.client.HTTPSConnection("harley-the-chatbot.p.rapidapi.com")
headers = {
    'content-type': "application/json",
    'Accept': "application/json",
    'X-RapidAPI-Key': "85632300dbmsha01f5765f1a7303p18df83jsn83e04aa1780a",
    'X-RapidAPI-Host': "harley-the-chatbot.p.rapidapi.com"
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


def filter_word(word):
    res = [ele for ele in blocked_list if (ele in word)]
    if res:
        return []
    word = ''.join(sorted(set(word), key=word.index))
    res = [ele for ele in blocked_names if (ele in word)]
    return res


def search_youtube_url(videoQuery):
    videosSearch = VideosSearch(f'{videoQuery}', limit = 5)
    if len(videosSearch.result()['result']) >= 1:
       num = random.randrange(0, 5)
       return videosSearch.result()['result'][num]['link']
    return "🤖🦇 No matching video found"


def search_video_url(videoQuery):
    ftr = [3600,60,1]
    url = ''

    videosSearch = VideosSearch(f'{videoQuery} 30 seconds', limit = 5)
    videos = videosSearch.result()['result']
    for i in range(len(videos)):
        duration = videos[i]['duration']
        timestr = duration
        if duration is not None:
            timestr = duration if len(duration.split(':')) >= 3 else f"00:{duration}"
        checkDuration = sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]) if timestr is not None else "None"
        if checkDuration <= 60: 
            url = videos[i]['link']
            break
    return url

class Bot:
    def __init__(self, contact):
        self.contact = contact
        elem = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, f'//*[text() = "{self.contact}" ]')))
        elem.click()
        self.incoming = WebDriverWait(driver, 120).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR ,'._aacl._aaco._aacu._aacx._aad6._aade')))
        self.received_msgs = len(self.incoming)
        self.running = True
        self.pressed_ctrl = False

    def make_call(self, request):
        
        payload = {
	        "client": "",
	        "bot": "harley",
	        "message": request
        }

        try:
            conn.request("POST", "/talk/bot", json.dumps(payload), headers)
            res = conn.getresponse()
            data = res.read()
            response = json.loads(data.decode("utf-8"))['data']['conversation']['output']
        except socket.timeout:
            return "ERR: Slow Internet connect on host"
        except http.client.HTTPException:
            self.make_call(request)
        else:  # no error occurred
            return response.replace('Harley', 'RAZBot').replace('robomatic.ai', 'instagram.com/raz0229')  # replace name and location in response

    def new_msg_received(self):
        incoming = driver.find_elements_by_css_selector('._aacl._aaco._aacu._aacx._aad6._aade')
        if len(incoming) != self.received_msgs:
            return True
        else:
            return False

    def send_message(self, text):
        input_box = driver.find_element_by_css_selector('textarea')
        input_box.click()
        input_box.send_keys(text, Keys.RETURN)
        incoming = driver.find_elements_by_css_selector('._aacl._aaco._aacu._aacx._aad6._aade')
        self.received_msgs = len(incoming)

    def send_copied_image(self):
        input_box = driver.find_element_by_css_selector('textarea')
        input_box.click()
        input_box.send_keys(Keys.LEFT_CONTROL, "v")
        send_button = driver.find_element_by_css_selector("._acan._acap._acaq._acas._acav")
        send_button.click()
        incoming = driver.find_elements_by_css_selector('._aacl._aaco._aacu._aacx._aad6._aade')
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

                    try:
                        self.incoming = driver.find_elements_by_css_selector('._aacl._aaco._aacu._aacx._aad6._aade')
                        self.received_msgs = len(self.incoming)
                        last_msg = self.incoming[self.received_msgs - 1].text
                        print(last_msg)
                    except Exception:
                        last_msg = 'Something exception'

                    # BOT response
                    if last_msg.lower().startswith("bot_ask"):
                        self.send_message('Thinking... 🤖🦇')

                        if deemojify(last_msg.lower().strip()) == "bot_ask":
                            self.send_message("🤖🦇 Chat with me using bot_ask command. Example: bot_ask who are you")
                        else:
                            self.send_message(self.make_call(deemojify(last_msg.replace("bot_ask", '').strip())))

                    # invalid command
                    elif last_msg.lower().startswith("bot "):
                        self.send_message('Invalid command 🤖🦇')

                    # initialize bot
                    elif last_msg.lower().startswith("bot_start"):
                        self.send_message('Bot Online 🤖🦇')
                        os.system(
                            "xclip -selection clipboard -t image/png -i ~/Documents/python-instagram-command-bot/commands.png")
                        self.send_copied_image()

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
                            self.send_message(response[0:500])

                    # Fancy text converter
                    elif last_msg.lower().startswith("bot_fancy"):
                        text = deemojify(last_msg.lower().replace("bot_fancy", "").strip())
                        if (filter_word(text)):
                            self.send_message("🤖🦇 OFFENSIVE WORDS BLOCKED BY CREATOR")
                        else:
                            fn = Fancy(text)
                            for i in range(25):
                                self.send_message(fn.makeFancy(i + 1))

                    # random insult thrower
                    elif last_msg.lower().startswith("bot_insult"):
                        name = deemojify(last_msg.lower().replace("bot_insult", "").strip())
                        if (filter_word(name)):
                            self.send_message("🤖🦇 OFFENSIVE WORDS BLOCKED BY CREATOR")
                        else:
                            f = open('insults.txt')
                            lines = f.readlines()
                            choice = random.randint(0, len(lines) - 1)
                            self.send_message(lines[choice].replace("XXX", name))

                    # random pickup line
                    elif last_msg.lower().startswith("bot_pickup"):
                        f = open('pickup.txt')
                        lines = f.readlines()
                        choice = random.randint(0, len(lines) - 1)
                        self.send_message(lines[choice])

                    # Anime quote
                    elif last_msg.lower().startswith("bot_quote"):
                        try:
                            quote = asyncio.run(waifu.quote())
                            self.send_message(quote["quote"])
                        except Exception:
                            self.send_message("🤖🦇 Cannot get Quote due to slow internet")
                    
                    # YouTube search
                    elif last_msg.lower().startswith("bot_yt"):
                        search = deemojify(last_msg.lower().replace("bot_yt", "").strip())
                        self.send_message(f"🤖🦇 Searching YouTube for: {search}")
                        self.send_message(search_youtube_url(search))
# url = search_video_url('sea shanty')        
# if url == '':
#     print("Video either too long or not exists")
# else:
#     print(url)
#     os.system("rm -rf song.mp3 song.mp4")
#     os.system(f"yt-dlp --extract-audio --audio-format mp3 --audio-quality 7 \"{url}\" -o song.mp3")
#     os.system("ffmpeg -loop 1 -i speaker.png -i song.mp3 -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\" -c:a copy -c:v libx264 -shortest song.mp4")


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

                    # Fetch image
                    elif last_msg.lower().startswith("bot_image"):
                        searchTerm = deemojify(last_msg.lower().replace("bot_image", "").strip())
                        if len(searchTerm) == 0:
                            self.send_message("🤖🦇 Please enter a search term too e.g bot_image Butterfly")
                        else:
                            self.send_message(f"🤖🦇 Fetching image for: {searchTerm}")
                            while True:
                                try:
                                    service = build("customsearch", "v1",
                                                    developerKey="AIzaSyB4hl9a1RPB_MmuqPm_zNmO49Y20qSf9e4")
                                    res = service.cse().list(
                                        q=slugify(searchTerm),
                                        cx='7204b6b1decb42058',
                                        searchType='image',
                                        imgSize="MEDIUM",
                                        safe='high'
                                    ).execute()

                                    if not 'items' in res:
                                        self.send_message("🤖🦇 Could not find any matching image")
                                    else:
                                        length = len(res['items'])
                                        load_requests(res['items'][randint(0, length - 1)]['link'], "image.png")
                                        os.system(
                                            "xclip -selection clipboard -t image/png -i ~/Documents/python-instagram-command-bot/image.png")
                                        self.send_copied_image()
                                        break

                                except Exception as ex:
                                    print(ex)
                                    self.send_message("Cannot find matching images")
                                    continue

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
