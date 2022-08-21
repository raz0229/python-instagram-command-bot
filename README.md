# 🤖 Python Instagram Command Bot
This repository is a fork of [Python WhatsApp Chatbot](https://github.com/raz0229/python-whatsapp-chatbot) built using Selenium and some 3rd party APIs from [RapidAPI](https://rapidapi.com) originally made to talk to your DMs on Instagram and give automatic replies but this feature has been confined to a separate mode i.e. *Chat Mode*.
The bot in *Standard Mode* comes with a total of 12 commands and only responds when triggered in your chats.

## 🦇🤖 Commands

 1. **BOT_ASK _something_** \
	 Responds to the user using either Aeona or Harley.
	 
 2. **BOT_ENGLISH _bonjour_** \
 Detects language and translates the passed text to English using Google Translate.
 3. **BOT_URDU _hello_** \
 Detects language and translates the passed text to Urdu using Google Translate. 
 4. **BOT_PASHTO _hello_** \
 Detects language and translates the passed text to Pashto using Google Translate.
 5. **BOT_WIKI _donald trump_** \
 Searches Wikipedia for the passed argument and sends a 9 lines description of it.
 6. **BOT_FANCY _your name_** \
 Spams the DM with 24 different ASCII styled variants of passed argument.
 7. **BOT_QUOTE** \
 Sends a random quote of a famous personality using _'quotes'_ PyPi package.
 8. **BOT_WAIFU** \
 Sends image of an SFW Waifu (by default) using _'waifu_pypics'_ PyPi package.
 9. **BOT_INSULT _your name_** \
 Throws a random insult of the name passed using _'insults.txt'_ in the root of your project.
 

> Add or remove insults from _'insults.txt'_ and replace the generic name with _XXX_.

 11. **BOT_PICKUP**  \
 Throws a random pickup line from _'pickup.txt'_ in the root of your project.
 12. **BOT_IMAGE _butterfly_**  \
 Sends an image of the argument passed using Google Custom Search API.
 
 13. **BOT_YT _lovely song_**  \
 Sends link and description of the passed argument using _'youtube-search'_ PyPi package. 
 
 

> (All the commands listed here and CASE-INSENSITIVE) 

## ❓ Usage

    Usage: main.py [Case-sensitive chat name] [OPTION]...

	DESCRIPTION
    Instagram command bot and chat bot. 
    
    -c, --chat
        This argument is REQUIRED. It is case-sensitive so the name of chat must match with the passed argument.

    -H, --headless 
        start bot in Headless mode. (No GUI)

    -C, --chatmode=[MALE|FEMALE]
        start bot in Chat mode. (Respond to all messages by default)
        --chat-mode=MALE : Talk to Harley
        --chat-mode=FEMALE : Talk to Aeona

	EXAMPLES
    python main.py -c "Chat Name"
        command bot is activated for chat "Chat Name".

    python main.py -c "Chat Name" --chatmode=FEMALE
        chat bot is activated for "Chat Name" for Aeona.

    python main.py -c "Chat Name" --chatmode=MALE --headless=True
        chat bot is activated for "Chat Name" for Harley in headless mode.


## ⚙️ Configuration and Run

 - Clone the repository and `cd` into it. \
 `git clone https://github.com/raz0229/python-instagram-command-bot.git`
  `cd python-instagram-command-bot`
 - Install all the dependencies \
 `pip install -r requirements.txt`
 - Download Geckodriver(https://github.com/mozilla/geckodriver/releases) for your FireFox web browser.

 > ( Mozilla Firefox browser is required )

 - Sign up for [RapidAPI](https://rapidapi.com), then create a `.env` file in the root of your project.
 `touch .env`
 
 In `.env` file, we need to set these environment variables:
 ```
    FIRST_NAME="Raz"
	FIREFOX_EXECUTABLE_PATH="/usr/bin/firefox"
	FIREFOX_PROFILE_LOCATION=""
	GECKODRIVER_PATH=""
	X_RAPIDAPI_KEY=""
	AEONA_USER_ID=""
	GOOGLE_CUSTOM_SEARCH_DEVELOPER_KEY=""
	GOOGLE_CUSTOM_SEARCH_CX=""
```

### 🔗 Useful Links

- To find your `X_RAPIDAPI_KEY`: \
    https://docs.rapidapi.com/docs/keys

- To find, your `AEONA_USER_ID`: \
    https://rapidapi.com/multiii/api/aeona3/

- To find, your `GOOGLE_CUSTOM_SEARCH_DEVELOPER_KEY` and `GOOGLE_CUSTOM_SEARCH_CX`: \
    https://console.cloud.google.com/marketplace/product/google/customsearch.googleapis.com

- `FIREFOX_PROFILE_LOCATION` would be somewhere in `%APPDATA%` for Windows and `$HOME/.mozilla/firefox` in Linux