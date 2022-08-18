# see 'main.py'
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium import webdriver
from waifu_pypics import Waifu
from pynput import keyboard
from slugify import slugify
from fancy import Fancy
import pyautogui as gui
from random import randint
import time
import http.client
import wikipedia
import asyncio
import requests
from googletrans import Translator
import socket
import emoji
import random
from quotes import Quotes
import json
import urllib.request
import signal
import sys
import re
import gc
import os
from selenium.webdriver.firefox.options import Options
from apiclient.discovery import build
from youtube_search import YoutubeSearch
#from youtubesearchpython import VideosSearch
from dotenv import load_dotenv

translator = Translator()
waifu = Waifu()
quotes = Quotes()

# Download block list to block obscene language and insults
print('[INFO] Downloading blocked keywords list..')
r = requests.get('https://jsonkeeper.com/b/5ULD')
list = r.json()

params = ['waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug', 'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush', 'smile', 'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'slap', 'kill', 'kick', 'happy', 'wink', 'poke', 'dance', 'cringe']
blocked_list = list['blocked_list']
blocked_names = list["blocked_names"]
print('[INFO] Blocklist Loaded into bot')

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

def search_youtube_url(videoQuery):
    # videosSearch = VideosSearch(f'{videoQuery}', limit = 5)
    # if len(videosSearch.result()['result']) >= 1:
    #    num = random.randrange(0, 5)
    #    return videosSearch.result()['result'][num]['link']
    # return "🤖🦇 No matching video found"
    results = YoutubeSearch(videoQuery, max_results=6).to_dict()
    ran = results[random.randint(0, 5)]
    return ran['title'], ran['channel'], ran['views'], ran['duration'], 'https://www.youtube.com' + ran['url_suffix']

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


def getTranslation(abv, text):
    try:
        response = translator.translate(text, dest=abv).text
    except Exception:
        print(f"\n🤖🦇: Error translating in {abv}")
        return
    else:
        return response


class Bot:

    def __init__(self, contact, HEADLESS=False):

        self.contact = contact
        self.HEADLESS = HEADLESS
        
        load_dotenv()
        options = Options()
        options.binary_location = os.getenv('FIREFOX_EXECUTABLE_PATH')
        options.add_argument("--window-size=1920,1080")
        options.headless = self.HEADLESS

        profile = FirefoxProfile(os.getenv('FIREFOX_PROFILE_LOCATION'))

        # Configuration
        self.FIRST_NAME = os.getenv("FIRST_NAME")
        PATH = os.getenv("GECKODRIVER_PATH")  # path to your downloaded webdriver
        self.driver = webdriver.Firefox(profile, executable_path=PATH, options=options)
        print('[INFO] Loading your chats...')
        self.driver.get('https://instagram.com/direct/inbox')
        # prints title of the webpage
        print("[INFO] " + self.driver.title + " loaded successfully")

        self.conn = http.client.HTTPSConnection("harley-the-chatbot.p.rapidapi.com")
        self.headers = {
            'content-type': "application/json",
            'Accept': "application/json",
            'X-RapidAPI-Key': os.getenv("HARLEY_CHATBOT_API_KEY"),
            'X-RapidAPI-Host': "harley-the-chatbot.p.rapidapi.com"
        }

        elem = WebDriverWait(self.driver, 120).until(EC.element_to_be_clickable((By.XPATH, f'//*[text() = "{self.contact}" ]')))
        try:
            notification_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Turn On')]")
            if notification_button:
                notification_button.click()
        except Exception:
            print('[LOG] Could not locate notification button')
        elem.click()
        print("[INFO] Bot running on chat: " + self.contact)
        self.incoming = WebDriverWait(self.driver, 120).until(
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
            self.conn.request("POST", "/talk/bot", json.dumps(payload), self.headers)
            res = self.conn.getresponse()
            data = res.read()
            response = json.loads(data.decode("utf-8"))['data']['conversation']['output']
        except socket.timeout:
            return "ERR: Slow Internet connect on host"
        except http.client.HTTPException:
            self.make_call(request)
        else:  # no error occurred
            return response.replace('Harley', 'RAZBot').replace('robomatic.ai', 'instagram.com/raz0229')  # replace name and location in response

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

    def send_copied_image(self):
        input_box = self.driver.find_element(By.CSS_SELECTOR,'textarea')
        #input_box = driver.find_element(By.CSS_SELECTOR, '._ab8w._ab94._ab99._ab9f._ab9m._ab9o._abbh._abcm textarea')
        input_box.click()
        #input_box.send_keys(os.getcwd()+"/image.png")
        #input_box.send_keys(Keys.RETURN)
        #os.system("xdotool type $(xclip -o -selection clipboard)")
        input_box.send_keys(Keys.LEFT_CONTROL, "v")
        #gui.hotkey('ctrl', 'v')
        send_button = self.driver.find_element(By.CSS_SELECTOR,"._acan._acap._acaq._acas._acav")
        #send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "._acan._acap._acaq._acas._acav")))
        send_button.click()
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
                        print("[INFO] New message: " + last_msg)
                    except Exception:
                        last_msg = 'Something exception'

                    # BOT response
                    if last_msg.lower().startswith("bot_ask"):
                        self.send_message('Thinking... 🤖🦇')

                        if deemojify(last_msg.lower().strip()) == "bot_ask":
                            self.send_message("🤖🦇 Chat with me using bot_ask command. Example: bot_ask who are you")
                        else:
                            self.send_message(self.make_call(deemojify(last_msg.replace("bot_ask", '').strip())))

                    # raz is offline
                    elif last_msg.lower().find(self.FIRST_NAME.lower()) != -1:
                        self.send_message('🤖🦇 Hi! {} is offline and I\'m in command. Please leave a message and I\'ll let him know'.format(Fancy(self.FIRST_NAME).makeFancy(1)))

                    # initialize bot
                    elif last_msg.lower().startswith("bot_start"):
                        self.send_message('Bot Online 🤖🦇')
                        os.system(
                            "xclip -selection clipboard -t image/png -i ~/Documents/python-instagram-command-bot/commands.png")
                        self.send_copied_image()

                    # Translate to Pashto
                    elif last_msg.lower().startswith("bot_pashto"):
                        dataPashto = getTranslation('ps', last_msg.lower().replace('bot_pashto', '').strip())
                        self.send_message("🤖🦇 Translating last message to Pashto...")
                        self.send_message(dataPashto)

                    # Translate to English
                    elif last_msg.lower().startswith("bot_english"):
                        dataEng = getTranslation('en', last_msg.lower().replace('bot_english', '').strip())
                        self.send_message("🤖🦇 Translating last message to English...")
                        self.send_message(dataEng)

                    # Translate to Urdu
                    elif last_msg.lower().startswith("bot_urdu"):
                        dataUr = getTranslation('ur', last_msg.lower().replace('bot_urdu', '').strip())
                        self.send_message("🤖🦇 Translating last message to Urdu...")
                        self.send_message(dataUr)

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
                            person, quote = quotes.random()
                            self.send_message(quote)
                            self.send_message('~ ' + person)
                        except Exception:
                            self.send_message("🤖🦇 Cannot get Quote due to slow internet")
                    
                    # YouTube search
                    elif last_msg.lower().startswith("bot_yt"):
                        search = deemojify(last_msg.lower().replace("bot_yt", "").strip())
                        if (filter_word(search)):
                            self.send_message("🤖🦇 EXPLICIT WORDS BLOCKED BY CREATOR")
                        else:
                            self.send_message(f"🤖🦇 Searching YouTube for: {search}")
                            title, channel, views, duration, url = search_youtube_url(search)
                            self.send_message('Title: ' + title)
                            self.send_message('Channel: ' + channel)
                            self.send_message('Views: ' + views)
                            self.send_message('Duration: ' + duration)
                            self.send_message('Link: ' + url)
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
                            waf = waifu.get_image(random.choice(params))
                            load_requests(waf, "waifu.png")
                            os.system("xclip -selection clipboard -t image/png -i " + os.getcwd() + "/waifu.png")
                            self.send_copied_image()
                            self.send_message(waf)
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
                                                    developerKey=os.getenv("GOOGLE_CUSTOM_SEARCH_DEVELOPER_KEY"))
                                    res = service.cse().list(
                                        q=slugify(searchTerm),
                                        cx=os.getenv("GOOGLE_CUSTOM_SEARCH_CX"),
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
                                            "xclip -selection clipboard -t image/png -i " + os.getcwd() + "/image.png")
                                        self.send_copied_image()
                                        break

                                except Exception as ex:
                                    print(ex)
                                    self.send_message("Cannot find matching images")
                                    continue

                                            
                    # raz is offline
                    elif last_msg.lower().find("bot") != -1:
                        self.send_message('Invalid command 🤖🦇')
                        os.system("xclip -selection clipboard -t image/png -i " + os.getcwd() + "/commands.png")
                        self.send_copied_image()


                    else:
                        print("No command")
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


