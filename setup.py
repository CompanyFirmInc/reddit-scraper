import webbrowser
import os
import sys
import time
import webbrowser
import configparser

def _setup_wizard(config) -> None:
    '''Setup via user input'''
    config['DEFAULT']['path'] = os.path.join(os.path.abspath,'scraper.py')
    print(f"Creating {config['DEFAULT']['path']}")

    config['DEFAULT']['timeout'] = 15
    cfg = config['scraper']
    cfg['client_secret'] = ""
    cfg['bot_version'] = "1.1.0"
    cfg['bot_author'] = ""
    cfg['client_id'] = ""
    cfg['user_agent'] = "%(bot_name)s:v%(bot_version)s (by u/%(bot_author)s)"

    with open('scraper.ini', 'w') as cf:
        print(f"Writing {}")
        config.write(cf)


def _load_from_ini(filename='./scraper.ini') -> dict:
    '''loads PRAW config from ini file'''
    config = configparser.ConfigParser()
    config.read(filename)
    
    # store in file data in dict
    ini_data = {"id":           config["scraper"]['client_id'],
                "secret":       config["scraper"]['client_secret'],
                "user_agent":   config["scraper"]['user_agent'],
                "timeout":      config["DEFAULT"]['timeout']}
    
    return ini_data


def setup() -> dict:
    '''Checks whether user has configured the program correctly'''
    filename = "./scraper.ini"
    
    config = configparser.ConfigParser()
    
    if os.path.exists(filename):
        return

    else:
        print("Performing the 'no .ini' setup procedure...")
        print(f"""Please sign into reddit and register a bot. 
        Enter the bot's details into {filename} which was
        just generated for your convenience. You will need the:
        client_id, client_secret and author_name. The program
        will complete the rest.""")
        time.sleep(2)

        webbrowser.open("https://www.reddit.com/prefs/apps")
        
        try:
            _setup_wizard(config)
        except:
            sys.exit()

        return _load_from_ini()

        