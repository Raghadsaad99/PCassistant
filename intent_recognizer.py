import re

# --- Keyword Groups ---
DIM_WORDS = ["lower", "decrease", "dim", "down", "reduce", "less"]
BRIGHTEN_WORDS = ["higher", "increase", "brighten", "up", "more"]
VOLUME_DOWN_WORDS = ["lower", "decrease", "quiet", "down", "reduce", "less"]
VOLUME_UP_WORDS = ["higher", "increase", "loud", "up", "more"]

# --- Helpers ---
def contains_any(keywords, text):
    return any(word in text for word in keywords)

def extract_number(text):
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None

# --- Intent Recognizer ---
def recognize_intent(text: str) -> tuple:
    lowered = text.lower()

    # --- Web Search ---
    if "search" in lowered and "google" in lowered:
        return "system", "googleSearch"
    elif "youtube" in lowered or ("play" in lowered and any(w in lowered for w in ["song", "video", "music"])):
        return "system", "youtube"
    
    # --- Screenshot ---
    elif "screenshot" in lowered or "take a screenshot" in lowered:
        return "system", "screenShot"

    # --- Word ---
    elif "start word" in lowered or "open word" in lowered or "word project" in lowered:
        return "system", "startWordProject"

    # --- Brightness ---
    elif "brightness" in lowered and contains_any(DIM_WORDS, lowered):
        return "system", "lowerBrightness"
    elif "brightness" in lowered and contains_any(BRIGHTEN_WORDS, lowered):
        return "system", "higherBrightness"
    elif "set brightness to" in lowered and extract_number(lowered) is not None:
        return "system", "setBrightness"

    # --- Volume ---
    elif "volume" in lowered and contains_any(VOLUME_DOWN_WORDS, lowered):
        return "system", "lowVolume"
    elif "volume" in lowered and contains_any(VOLUME_UP_WORDS, lowered):
        return "system", "highVolume"
    elif "mute" in lowered and "volume" in lowered:
        return "system", "muteVolume"
    elif "unmute" in lowered and "volume" in lowered:
        return "system", "unmuteVolume"
    elif "set volume to" in lowered and extract_number(lowered) is not None:
        return "system", "setVolume"

    # --- Download Placeholder ---
    elif "music" in lowered and "download" in lowered:
        return "system", "downloadMusic"

    # --- Fallback ---
    else:
        return "general", text

