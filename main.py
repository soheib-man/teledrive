import os
import sys


import telethon 
from telegram import Telegram
from termcolor import colored
from telethon import TelegramClient, events, sync

def main():

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))

    # See if `temp` directory exists
    temp_dir = os.path.join(ROOT_DIR, "temp")
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    else:

        # Clean
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))

    # Check if `config.json` exists
    config_file = "c:/Users/DELL/OneDrive/Desktop/teledrive/config.json"

    if not os.path.exists(config_file):
        print(colored("[-] Couldn't not find your config file.", "red"))
        sys.exit(1)

    telegram = Telegram()

    # See args
    args = sys.argv[1:]
    print(args)
    command = args[0]

    if len(args) == 0:
        print(colored("[-] No arguments provided.", "red"))
        sys.exit(1)

    if command == "upload":
        if len(args) < 2:
            print(colored("[-] Not enough arguments provided.", "red"))
            sys.exit(1)
        
        current_dir = os.getcwd()
        file_path = args[1] # File path after `upload` command
        file_name = os.path.basename(file_path)
        

        if not os.path.exists(file_path):
            print(colored(f"[-] File {file_path} does not exist.", "red"))
            sys.exit(1)

        # Check if directory
        if os.path.isdir(file_path):
            # Upload as directory

            telegram.upload_directory(current_dir, file_path, file_name)
            sys.exit(0)
        else:
            # Upload as file
            print(os.path.join(current_dir,file_path))
            telegram.upload_file(current_dir, file_path, file_name)
            
            sys.exit(0)
    if command == "download":
        if len(args) < 2:
            print(colored("[-] Not enough arguments provided.", "red"))
            sys.exit(1)

        file_query = args[1]
        telegram.download_file(file_query)

        sys.exit(0)

    if args[0] == "list":
        telegram.list_files()

        sys.exit(0)

    if command == "remove":
        if len(args) < 2:
            print(colored("[-] Not enough arguments provided.", "red"))
            sys.exit(1)

        file_query = args[1]
        telegram.remove_file(file_query)

        sys.exit(0)

    print(colored(f"[-] Invalid action {args[0]}.", "red"))
    sys.exit(1)


if __name__ == "__main__":
    main()