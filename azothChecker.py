import os
import subprocess
import wizwalker
import asyncio
import pyautogui
from wizwalker import Client, client
from wizwalker.constants import Keycode
from wizwalker.memory import Window
from wizwalker.utils import get_all_wizard_handles, start_instance, instance_login
from wizwalker import ClientHandler

spellbook = ["WorldView", "DeckConfiguration"]
playButton = ['WorldView', 'mainWindow', 'btnPlay']
quitButton = ['WorldView', 'DeckConfiguration', 'SettingPage', 'QuitButton']


async def is_visible_by_path(base_window:Window, path: list[str]):
    # Credit to SirOlaf for the original function; I'm modifying it - credit ultimate314
    if window := await window_from_path(base_window, path):
        return await window.is_visible()
    return False

# Returns a window, given a path 
async def window_from_path(base_window:Window, path:list[str]) -> Window:
    # Credit to SirOlaf for the original function; I'm modifying it - credit ultimate314;  and now me i have stolen this mwah haha - milwr i think?
    if not path:
        return base_window
    for child in await base_window.children():
        if await child.name() == path[0]:
            if found_window := await window_from_path(child, path[1:]):
                return found_window
    return False


async def click_window_from_path(mouse_handler, base_window, path): #credit ultimate314
    try:
        await mouse_handler.click_window(await window_from_path(base_window, path))
    except:
        pass

async def click_window_until_gone(client, path): #i did this im very cool - milwr (ithink)
    while (window := await window_from_path(client.root_window, path)) and await is_visible_by_path(client.root_window, path):
            await client.mouse_handler.click_window(window)
            await asyncio.sleep(0.1)





async def get_player_school(p) -> str: # FAJ MADE THIS ONE TOO, starr fixed it
    txtLevel = ['WorldView', 'mainWindow', 'sprSubBanner', 'txtLevel']
    window : Window = await window_from_path(p.root_window, txtLevel)
    if window:
      return await window.maybe_text()
    return ""




async def tc():
    center_location = pyautogui.locateCenterOnScreen('tc.png')
    
    return center_location


async def tc_button():
    tc_bttn = pyautogui.locateCenterOnScreen('tcbutton.png') # i dont know how to click sprites
    
    pyautogui.click(tc_bttn)
    
    await asyncio.sleep(0.1)
    
total_azoth_stacks = 0



async def main_checker(p):
    while not is_visible_by_path(p.root_window, spellbook):
        await p.send_key(Keycode.P)
        asyncio.sleep(0.1)
    asyncio.sleep(1)
    await tc_button()
    asyncio.sleep(0.5)
    if await tc() != "":
        total_azoth_stacks = total_azoth_stacks + 1
        print(total_azoth_stacks)
    else:
        pass
    while not await is_visible_by_path(p.root_window, quitButton):
        await p.send_key(Keycode.ESC, 0.05)
    if await is_visible_by_path(p.root_window, quitButton):
        await click_window_from_path(p.mouse_handler, p.root_window, quitButton)
    


async def logic(p):
    await setup(p)
    wizards = [] # create list for all wizards
    wizard = await get_player_school(p) # current wizard on the screen school is captured
    print(await get_player_school(p))
    wizard = wizard.split(' ')
    #wizard[3] = wizard[3].replace(')', '') # changes ex. level 160 (prime diviner), to 160 diviner
    length = len(wizards)
    while wizard != "" and length != 6: # when the school isnt blank, idk why i added this tbh..., this should add all 6 wizards to the list then stop, if u have 7 on a storage acc for some rzn, change it to 7
        if wizard not in wizards: # if the current wizard is not already in the list
            wizards.append(wizard)    # add it
            await p.send_key(Keycode.TAB, 0.1) # go to next wizard
    print("Checking for azoth stacks on", wizards)
    time = 0
    for i in range(length):
        while wizard != wizards[time]:
            await p.send_key(Keycode.TAB, 0.1)
        if wizard == wizards[time]:
            await p.click_window_until_gone(p.mouse_handler, p.root_window, playButton)
            await asyncio.sleep(8)
            await main_checker(p)
            time = time + 1
    subprocess.call(f"taskkill /F /PID {p.process_id}",stdout=subprocess.DEVNULL) #kills the current wizard client

            

async def setup(p): #activates all hooks that it can for a client
    print("Activating Special Lxghtend Hooks :o :p :3")
    await p.hook_handler.activate_root_window_hook(wait_for_ready=False)
    await p.hook_handler.activate_render_context_hook(wait_for_ready=False)
    await p.mouse_handler.activate_mouseless()


async def startup():
    print("""
    Azoth Checker By Lxghtend      
    Credits:
    Milwr - used A LOT of his code in this bot
    Notfaj - helpin as always :3
              """) 
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"accounts.txt")) as my_file:
            accountList = [
                line.strip().split(":") for line in my_file.read().split("\n") #reads account list and puts into into a list
                ]
            for i in range(len(accountList)):
                handles = get_all_wizard_handles()
                start_instance()
                await asyncio.sleep(10)
                handle = list(set(get_all_wizard_handles()).difference(handles))[0] #finds the new handle made by start_instance()
                instance_login(handle, accountList[i][0], accountList[i][1])
                p = Client(handle) #defines a client
                await asyncio.sleep(5)
                await p.send_key(Keycode.P)
                await asyncio.sleep(10)
                await logic(p) 








asyncio.run(startup())
