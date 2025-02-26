import asyncio

# from modules.notifybot import ready_event, send_message, start_bot, close_bot

import pyautogui
import keyboard


async def FindImage(file_name, confidence, interval=0, limit=0):
    for _ in iter(int, 1) if limit == 0 else range(limit):
        try:
            location = await asyncio.to_thread(pyautogui.locateOnScreen, f"./Images/{file_name}", grayscale=True, confidence=confidence) # using the confidence parameter will force to use _locateAll_opencv() instead of _locateAll_pillow()
            return location
        except pyautogui.ImageNotFoundException:
            if (interval > 0):
                await asyncio.sleep(interval)
            continue
    
    return None


async def Buyout():
    # attempt to buyout
    pyautogui.press("down")
    pyautogui.press("enter")
    await asyncio.sleep(0.1)
    pyautogui.press("enter")

    # wait for the Buyout message and press Enter
    await asyncio.sleep(0.2)
    await FindImage("Enter.png", 0.9, interval=0.1)
    pyautogui.press("enter")

    await asyncio.sleep(0.2)
    pyautogui.press("esc")
    await asyncio.sleep(0.2)


def DetectBuyKey():
    while True:
        key_event = keyboard.read_event(suppress=False)
        if key_event.name == 'b' and key_event.event_type == keyboard.KEY_DOWN:
            return True
        elif key_event.name == 'n' and key_event.event_type == keyboard.KEY_DOWN:
            return False


async def Macro(interrupt_event, advanced_search=False, halfauto=False, halfauto_scroll=60):
    advanced_search |= halfauto
    pyautogui.moveTo(1, 1) # move the cursor to the top left corner to prevent interference

    while interrupt_event.is_set() == False:
        pyautogui.press("enter")
        await asyncio.sleep(0.13)
        if advanced_search:
            pyautogui.press('x')
            await asyncio.sleep(0.13)
        pyautogui.press("enter")

        if advanced_search: # advanced search takes longer to load
            await asyncio.sleep(0.78)
        else:
            await asyncio.sleep(0.64)

        if halfauto:
            pyautogui.press("down", presses=halfauto_scroll, interval=0.01) # scroll down to the fresh 59m auctions
            if await asyncio.to_thread(DetectBuyKey):
                pyautogui.press('y')
                await asyncio.sleep(0.1)
                await Buyout()
            else:
                pass
        else:
            if await FindImage("Y.png", 0.75, limit=1) != None: # if search result is not empty
                # spam the Y key
                while True:
                    pyautogui.press('y')
                    if await FindImage("Y.png", 0.75, limit=1) == None:
                        break
                await Buyout()

        pyautogui.press("esc")
        await asyncio.sleep(0.6)


async def Stopper(interrupt_event):
    while interrupt_event.is_set() == False:
        await asyncio.sleep(0.1)
        if await asyncio.to_thread(keyboard.is_pressed, "F2"): # run the blocking function in a separate thread
            interrupt_event.set()
            print("Script will be stopped after the current loop.")
            # await send_message("Script will be stopped after the current loop.")


async def main():
    """ # start the bot
    bot_task = asyncio.create_task(start_bot())
    await ready_event.wait()  # wait until the bot is ready """

    # wait for F1 key to start
    print("Script ready. Press F1 to start the script.")
    # await send_message("Script ready.")
    await asyncio.to_thread(keyboard.wait, "F1") # run the blocking function in a separate thread
    print("Script started.")
    # await send_message("Script started.")

    interrupt_event = asyncio.Event()
    await asyncio.gather(Macro(interrupt_event), Stopper(interrupt_event))

    print("Exiting the script.")
    # await send_message("Exiting the script.")

    # await close_bot()


if __name__ == "__main__":
    asyncio.run(main())