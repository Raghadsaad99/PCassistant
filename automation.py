import webbrowser
import pyautogui
import subprocess
import platform
import screen_brightness_control as sbc
import time

# --- Platform-specific imports/dummies ---
if platform.system() == "Windows":
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
else:
    pass  # no dummies needed since usage is guarded by platform checks


def google_search(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searching Google for: {query}"

def youtube_search(query):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
    return f"Searching YouTube for: {query}"

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
            return "Attempting to open Microsoft Word."
        elif system == "Darwin":  # macOS
            subprocess.Popen(['open', '-a', 'Microsoft Word'])
            return "Attempting to open Microsoft Word."
        elif system == "Linux":
            return "Opening Word is not natively supported on Linux. Try LibreOffice Writer."
        else:
            return f"Word automation not supported on {system}."
    except FileNotFoundError:
        return "Microsoft Word application not found."
    except Exception as e:
        return f"Failed to open Word: {e}"

# --- Brightness Control ---
def get_current_brightness():
    try:
        current = sbc.get_brightness(display=0)
        return current[0] if isinstance(current, list) else current
    except Exception as e:
        print(f"Error getting brightness: {e}")
        return None

def set_brightness(value):
    try:
        sbc.set_brightness(value, display=0)
        return f"Brightness set to {value}%."
    except Exception as e:
        return f"Failed to set brightness: {e}"

def lower_brightness(step=10):
    current = get_current_brightness()
    if current is not None:
        new_brightness = max(current - step, 0)
        return set_brightness(new_brightness)
    return "Failed to get current brightness."

def increase_brightness(step=10):
    current = get_current_brightness()
    if current is not None:
        new_brightness = min(current + step, 100)
        return set_brightness(new_brightness)
    return "Failed to get current brightness."

# --- Volume Control helpers ---
def run_osascript(script):
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        print(f"AppleScript error: {e}")
        return None

if platform.system() == "Windows":
    def get_master_volume_object():
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            return cast(interface, POINTER(IAudioEndpointVolume))
        except Exception as e:
            print(f"Error getting volume object: {e}")
            return None

def get_volume_percentage():
    system = platform.system()
    if system == "Windows":
        volume = get_master_volume_object()
        if volume:
            current_db = volume.GetMasterVolumeLevel()
            min_vol, max_vol, _ = volume.GetVolumeRange()
            if max_vol == min_vol:
                return 0 if current_db <= min_vol else 100
            percentage = ((current_db - min_vol) / (max_vol - min_vol)) * 100
            return int(round(percentage))
    elif system == "Darwin":
        result = run_osascript("output volume of (get volume settings)")
        if result and result.isdigit():
            return int(result)
    return None

def set_volume_percentage(percentage):
    if not 0 <= percentage <= 100:
        return "Percentage must be between 0 and 100."
    system = platform.system()
    if system == "Windows":
        volume = get_master_volume_object()
        if volume:
            min_vol, max_vol, _ = volume.GetVolumeRange()
            target_db = min_vol + (max_vol - min_vol) * (percentage / 100.0)
            try:
                volume.SetMasterVolumeLevel(target_db, None)
                return f"Volume set to {percentage}%."
            except Exception as e:
                return f"Failed to set volume: {e}"
        return "Failed to access Windows audio device."
    elif system == "Darwin":
        if run_osascript(f"set volume output volume {percentage}") is not None:
            return f"Volume set to {percentage}%."
        return "Failed to set volume on macOS."
    else:
        return "Setting volume percentage only supported on Windows and macOS."

def increase_volume(step=5):
    system = platform.system()
    if system in ["Windows", "Darwin"]:
        current = get_volume_percentage()
        if current is not None:
            new_vol = min(100, current + step)
            return set_volume_percentage(new_vol)
        return f"Failed to get current volume for precise increase on {system}."
    else:
        pyautogui.press('volumeup')
        return "Volume increased."

def decrease_volume(step=5):
    system = platform.system()
    if system in ["Windows", "Darwin"]:
        current = get_volume_percentage()
        if current is not None:
            new_vol = max(0, current - step)
            return set_volume_percentage(new_vol)
        return f"Failed to get current volume for precise decrease on {system}."
    else:
        pyautogui.press('volumedown')
        return "Volume decreased."

def mute_volume():
    system = platform.system()
    if system == "Windows":
        volume = get_master_volume_object()
        if volume:
            try:
                volume.SetMute(1, None)
                return "Volume muted."
            except Exception as e:
                return f"Failed to mute volume: {e}"
        return "Failed to access Windows audio device."
    elif system == "Darwin":
        if run_osascript("set volume with output muted") is not None:
            return "Volume muted."
        return "Failed to mute volume on macOS."
    else:
        pyautogui.press('volumemute')
        return "Volume muted (may toggle)."

def unmute_volume():
    system = platform.system()
    if system == "Windows":
        volume = get_master_volume_object()
        if volume:
            try:
                volume.SetMute(0, None)
                return "Volume unmuted."
            except Exception as e:
                return f"Failed to unmute volume: {e}"
        return "Failed to access Windows audio device."
    elif system == "Darwin":
        if run_osascript("set volume without output muted") is not None:
            return "Volume unmuted."
        return "Failed to unmute volume on macOS."
    else:
        return "Unmuting volume only precisely supported on Windows and macOS."


def execute_command(command, user_input=None):
    if command == "googleSearch":
        query = user_input.lower().replace("search", "").replace("google", "").replace("for", "").strip()
        return google_search(query) if query else "No query provided for Google search."

    elif command == "youtube":
        query = user_input.lower()
        for word in ["play", "on youtube", "youtube", "search"]:
            query = query.replace(word, "")
        query = query.strip()
        return youtube_search(query) if query else "Please provide something to search on YouTube."

    elif command == "screenShot":
        return take_screenshot()

    elif command == "startWordProject":
        return start_word_project()

    elif command == "lowerBrightness":
        return lower_brightness()

    elif command == "higherBrightness":
        return increase_brightness()

    elif command == "setBrightness":
        try:
            percentage = int(''.join(filter(str.isdigit, user_input)))
            return set_brightness(percentage)
        except ValueError:
            return "Invalid brightness percentage. Please say 'set brightness to [number]'."

    elif command == "lowVolume":
        return decrease_volume()

    elif command == "highVolume":
        return increase_volume()

    elif command == "muteVolume":
        return mute_volume()

    elif command == "unmuteVolume":
        return unmute_volume()

    elif command == "setVolume":
        try:
            percentage = int(''.join(filter(str.isdigit, user_input)))
            return set_volume_percentage(percentage)
        except ValueError:
            return "Invalid volume percentage. Please say 'set volume to [number]'."

    elif command == "downloadMusic":
        return "Download music feature is a placeholder."

    else:
        return "Unknown command."
