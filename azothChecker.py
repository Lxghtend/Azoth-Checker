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

total_azoth_stacks = 0
remainder_azoth = 0



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


    
async def check_tc(p):

    tc = ['WorldView', 'DeckConfigurationWindow', 'DeckPage', 'TreasureCardCount']

    window : Window = await window_from_path(p.root_window, tc)

    if window:
      return await window.maybe_text()
    return ""



async def main_checker(p):

    # Navigate to tc window
    while not is_visible_by_path(p.root_window, spellbook):
        await p.send_key(Keycode.P)
        await asyncio.sleep(0.1)

    # Create a variable for TC
    tc = await check_tc(p)
    tc = tc.replace("<center>", '').replace("</center>", '').replace("/999", '')
    tc = int(tc)

    # Add to the variable if stacks are found
    if tc == 999:
        total_azoth_stacks = total_azoth_stacks + 1
        print("Total Azoth (in stacks):", total_azoth_stacks)

    if tc << 999:
        remainder_azoth = remainder_azoth + tc
        print("Azoth Not In Full Stacks:", remainder_azoth)

    if tc == 0:
        print("No azoth found on current wizard.")
    
    # Quit out to prepare for the next wizard
    while not await is_visible_by_path(p.root_window, quitButton):
        await p.send_key(Keycode.ESC, 0.05)

    if await is_visible_by_path(p.root_window, quitButton):
        await click_window_from_path(p.mouse_handler, p.root_window, quitButton)
                


async def new_logic(p):

    # Attaches hooks
    await setup(p)

    # Defining lists that are used later
    wizards = []
    wizards_print = []

    # Add wizards to a list
    for i in range(6): # Repeats 6 times, if you have 7 characters for some reason, DM me on discord and ill make you a seperate version (@Lxghtend)

        wizard = await get_player_school(p)
        
        # This block simply formats text that is later displayed in the terminal (decorative)
        wizard_print = wizard.replace('<center>', '').replace('</center>', '')
        wizard_print = wizard_print.split(' ')
        wizard_print[3] = wizard_print[3].replace(')', '') # Changes ex. Level 160 (Prime Diviner), to 160 Diviner
        wizard_print = wizard_print[1], wizard_print[3]
        wizard_print = ' '.join(wizard_print)
        wizards_print.append(wizard_print)

        # Adds wizard to list wizards
        wizards.append(wizard)

        # Switch to the next wizard
        await p.send_key(Keycode.TAB)
        await asyncio.sleep(0.2)

    print("Azoth Checker is checking wizards:", wizards_print)

    time = 0

    # Runs the checker
    for i in range(6): # Repeats 6 times, if you have 7 characters for some reason, DM me on discord and ill make you a seperate version (@Lxghtend)

        wizard = await get_player_school(p)

        while wizard != wizards[time]:
            await p.send_key(Keycode.TAB, 0.1)
            wizard = await get_player_school(p)

        if wizard == wizards[time]:
            await click_window_until_gone(p.root_window, playButton)
            await asyncio.sleep(8)
            await main_checker(p)
            time = time + 1

    subprocess.call(f"taskkill /F /PID {p.process_id}",stdout=subprocess.DEVNULL) # Kills the current wizard client



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
    
    # This block starts, logs in, and defines a client but it confuses me so
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
                await new_logic(p) 




asyncio.run(startup())
