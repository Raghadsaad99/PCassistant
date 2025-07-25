import webbrowser
import pyautogui
import subprocess
import platform
import screen_brightness_control as sbc
import time

def google_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")

def youtube_search(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def take_screenshot():
    filename = f"screenshot_{int(time.time())}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    return f"Screenshot saved as {filename}"

def start_word_project():
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.Popen(['start', 'winword'], shell=True)
        elif system == "Darwin":
            subprocess.Popen(['open', '-a', 'Microsoft Word'])
        else:
            return "Word automation not supported on this OS."
        return "Microsoft Word opened."
    except Exception as e:
        return f"Failed to open Word: {e}"

def lower_brightness():
    try:
        current = sbc.get_brightness(display=0)[0]
        sbc.set_brightness(max(current - 10, 0))
        return "Brightness decreased."
    except Exception as e:
        return f"Failed to decrease brightness: {e}"

def increase_brightness():
    try:
        current = sbc.get_brightness(display=0)[0]
        sbc.set_brightness(min(current + 10, 100))
        return "Brightness increased."
    except Exception as e:
        return f"Failed to increase brightness: {e}"

def decrease_volume():
    try:
        pyautogui.press('volumedown')
        return "Volume decreased."
    except Exception as e:
        return f"Failed to decrease volume: {e}"

def increase_volume():
    try:
        pyautogui.press('volumeup')
        return "Volume increased."
    except Exception as e:
        return f"Failed to increase volume: {e}"

def execute_command(command, detail=None):
    if command == "googleSearch":
        if detail:
            google_search(detail)
            return "Google search opened."
        return "No query provided for Google search."

    elif command == "youtube":
        if detail:
            query = detail.lower().replace("search", "").replace("on youtube", "").replace("youtube", "").strip()
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Searching YouTube for: {query}"
        return "Please provide something to search on YouTube."

    elif command == "screenShot":
        return take_screenshot()

    elif command == "startWordProject":
        return start_word_project()

    elif command == "lowerBrightness":
        return lower_brightness()

    elif command == "higherBrightness":
        return increase_brightness()

    elif command == "lowVolume":
        return decrease_volume()

    elif command == "highVolume":
        return increase_volume()

    elif command == "downloadMusic":
        return "Download music feature is a placeholder."

    else:
        return "Unknown command."
