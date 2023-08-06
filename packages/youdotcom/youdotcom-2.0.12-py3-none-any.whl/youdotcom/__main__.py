# type: ignore[attr-defined]
from typing import Optional

import os
import sys
import time
from enum import Enum
from importlib import metadata as importlib_metadata
from random import choice
import subprocess
import requests
import typer
import pathlib
import glob
from click_shell import shell
from colorama import Fore
from rich.console import Console
import click
from click_shell import make_click_shell

import youdotcom

# from youdotcom import version


@shell(prompt="YouShell > ", intro="Welcome to YouShell an interactive shell for all YouDotCom commands\nEnter 'help' for a list of available commands.\nType 'exit' to stop.\n\n")
def app():
    pass


@app.command()
def Code():

    from youdotcom import Code  # import the write class

    inputstr = input("Enter a code completion prompt: ")
    print("Please wait...")
    text = Code.gen_code(f"{inputstr}")  # make an api call

    print(text["response"])  # print the AI made code

    print("Total time taken: " + text["time"])  # print total time taken to complete your request


@app.command()
def search():

    from youdotcom import Search  # import the Search class

    inputstr = input("Enter a search prompt: ")
    print("Please wait...")
    search_results = Search.search_for(f"{inputstr}")  # search! No need to use the Webdriver class.

    print(search_results["results"]["mainline"]["bing_search_results"])  # print all the search results

    print("Total time taken: " + search_results["time"])  # print total time taken to complete your request


@app.command()
def write():
    from youdotcom import Write  # import the write class

    inputstr = input("Enter a prompt: ")
    print("Please wait...")
    text = Write.write(f"{inputstr}")  # make an api call

    print(text["response"])  # print the AI made text

    print("Total time taken: " + text["time"])
    
    
@app.command()
@click.pass_context
def host(ctx):
    print(f"[API] - using context: {ctx}")
    p = subprocess.Popen(['pip', 'show', 'youdotcom'], stdout=subprocess.PIPE)
    out = p.stdout.read().decode("utf-8") 

    data = out.split("\n")
    for line in data:
        if line.startswith("Location: "):
            try: 
                path = str(line[10:]).replace("\\\\", "/")
            except:
                path = str(line[10:])
            print(path)
            path1 = glob.glob(f'{path}\\youdotcom\\api_1.py', recursive=True)[0]
            path2 = glob.glob(f'{path}\\youdotcom\\api_2.py', recursive=True)[0]
            
            
    print(f"[API] - using path {path1}\n{path2}")
    
    api = subprocess.Popen(["python",f"{path1}"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    backend = subprocess.Popen(["python",f"{path2}"])
    # api.terminate()
    # backend.terminate()
    


@app.command()
def chat():

    inputstr = input("Enter a message: ")
    webdriver = input("Enter webdriver_path (press enter for none): ")
    print("Please wait...")
    from youdotcom import Chat, Webdriver

    if webdriver:

        chat = Chat.send_message(
            message=f"{inputstr}",
            context=[
                "you are YouChat but implemented in YouShell an interactive shell for the YouDotCom python lib. Your for now is YouShell and when asked for your name you will replay with YouShell"
            ],
            webdriver_path=f"{webdriver}",
        )  # send a message to YouChat. passing the driver and messages
    else:
        chat = Chat.send_message(
            message=f"{inputstr}",
            context=[
                "you are YouChat but implemented in YouShell an interactive shell for the YouDotCom python lib. Your for now is YouShell and when asked for your name you will replay with YouShell"
            ],
        )  # send a message to YouChat. passing the driver and messages

    print(chat["message"])  # {'message': "It's been great! How about yours?", 'time': '11', 'error': 'False'}
    print(chat["time"])


@app.command()
def clear():
    try:
        os.system("clear")
    except:
        os.system("cls")
    


if __name__ == "__main__":
    app()
