# tremolog

Micro:blog via Telegram Bot

![Tremolog Home Screenshot](tremolog-home-screenshot.png)

### Status:

- 140 char text messages
- latest 10 posts
- yup 😅

## Install

Clone the git repo and install the dependencies:

```bash
git clone https://github.com/hiway/tremolog.git
cd tremolog
```

Create virtual environment for python3

    $ python3 -m venv venv  

Activate virtual environment
    
    $ source venv/bin/activate

Install dependencies
    
    $ pip install -e .  # Don't forget the dot!

Create a telegram app, and a bot. Get the api_id and api_hash from [my.telegram.org](https://my.telegram.org/apps) and get the bot token from [t.me/botfather](https://t.me/botfather)

Then, with the information handy, run the following command to create a config file:
    
    $ tremolog login

Run the app

    $ ./run.sh

Chat with your bot on Telegram.
