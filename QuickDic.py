import logging
import subprocess
import string
import re
import os
import pwnagotchi.plugins as plugins

'''
Aircrack-ng needed, to install:
> apt-get install aircrack-ng
Upload wordlist files in .txt format to folder in config file (Default: /opt/wordlists/)
Cracked handshakes stored in handshake folder as [essid].pcap.cracked
'''

class QuickDic(plugins.Plugin):
    __author__ = 'pwnagotchi [at] rossmarks [dot] uk'
    __version__ = '1.0.1'
    __license__ = 'GPL3'
    __description__ = 'Run a quick dictionary scan against captured handshakes'

    def __init__(self):
        self.text_to_set = ""

    def on_loaded(self):
        logging.info("Quick dictionary check plugin loaded")

        if 'face' not in self.options:
            self.options['face'] = '(·ω·)'

        try:
            check = subprocess.run(
                ['/usr/bin/dpkg', '-l', 'aircrack-ng'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if 'aircrack-ng' in check.stdout:
                logging.info("quickdic: Found aircrack-ng installed")
            else:
                logging.warning("aircrack-ng is not installed!")
        except Exception as e:
            logging.error(f"Error checking for aircrack-ng: {e}")

    def on_handshake(self, agent, filename, access_point, client_station):
        display = agent.view()

        try:
            # Check for handshake
            result = subprocess.run(
                ['/usr/bin/aircrack-ng', filename],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            if "1 handshake" not in result.stdout:
                logging.info("[quickdic] No handshake found")
                return

            logging.info("[quickdic] Handshake confirmed")

            # Get all .txt files from the wordlist folder
            wordlist_folder = self.options.get('wordlist_folder', '/opt/wordlists/')
            wordlists = [os.path.join(wordlist_folder, f) for f in os.listdir(wordlist_folder) if f.endswith('.txt')]

            if not wordlists:
                logging.warning("[quickdic] No wordlist files found")
                return

            # Execute aircrack-ng with all wordlist files
            for wordlist in wordlists:
                result2 = subprocess.run(
                    ['aircrack-ng', '-w', wordlist, '-l', filename + '.cracked', '-q', '-b', result.stdout.split()[1], filename],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                logging.info("[quickdic] " + result2.stdout.strip())

                if "KEY NOT FOUND" not in result2.stdout:
                    key_match = re.search(r'\[([^\]]+)\]', result2.stdout)
                    if key_match:
                        pwd = key_match.group(1)
                        self.text_to_set = f"Cracked password: {pwd}"
                        display.update(force=True)
                        plugins.on('cracked', access_point, pwd)
                        return  # Stop after finding the key

            logging.info("[quickdic] No key found in any wordlist")

        except Exception as e:
            logging.error(f"Error during handshake processing: {e}")

    def on_ui_update(self, ui):
        if self.text_to_set:
            ui.set('face', self.options['face'])
            ui.set('status', self.text_to_set)
            self.text_to_set = ""
