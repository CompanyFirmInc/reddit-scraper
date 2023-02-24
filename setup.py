import webbrowser
import os
import sys
import time
import webbrowser
import configparser

def _setup_wizard(config):
    '''Setup via user input'''
    config['DEFAULT']['path'] = os.path.join(os.path.abspath,'scraper.py')
    print(f"Creating {config['DEFAULT']['path']}")

    config['DEFAULT']['timeout'] = 15
    cfg = config['scraper']
    cfg['client_secret'] = ""
    cfg['bot_version'] = ""
    cfg['bot_author'] = ""
    cfg['client_id'] = ""

    with open('scraper.ini', 'w') as cf:
            config.write(cf)


def _load_from_ini(filename='./scraper.ini'):
    '''loads PRAW config from ini file'''
    config = configparser.ConfigParser()
    config.read(filename)
    
    # store in file data in dict
    ini_data = {"id":           config["scraper"]['client_id'],
                "secret":       config["scraper"]['client_secret'],
                "user_agent":   config["scraper"]['user_agent'],
                "timeout":      config["DEFAULT"]['timeout']}
    
    return ini_data


def setup():
    '''Checks whether user has configured the program correctly'''
    filename = "./scraper.ini"
    
    config = configparser.ConfigParser()
    
    if os.path.exists(filename):
        return

    else:
        print("Performing no `.ini` configuration...")
        time.sleep(2)

        webbrowser.open("https://www.reddit.com/prefs/apps")
        
        try:
            _setup_wizard(config)
        except:
            sys.exit()

        ini_data = _load_from_ini()

        