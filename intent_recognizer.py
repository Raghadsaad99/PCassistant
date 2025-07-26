import re

# Keywords for intent recognition
DIM_WORDS = ["lower", "decrease", "dim", "down", "reduce", "less"]
BRIGHTEN_WORDS = ["higher", "increase", "brighten", "up", "more"]
VOLUME_DOWN_WORDS = ["lower", "decrease", "quiet", "down", "reduce", "less"]
VOLUME_UP_WORDS = ["higher", "increase", "loud", "up", "more"]

def contains_any(keywords, text):
    """
    Check if any keyword from the list exists in the given text.

    Args:
        keywords (list): A list of keyword strings.
        text (str): Input text to check against.

    Returns:
        bool: True if any keyword is found in the text.
    """
    return any(word in text for word in keywords)

def extract_number(text):
    """
    Extract the first integer number from the input text.

    Args:
        text (str): The input string containing possible numbers.

    Returns:
        int or None: The first number found or None if not found.
    """
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None

def recognize_intent(text: str) -> tuple:
    """
    Recognize the user's intent based on natural language input.

    Args:
        text (str): The user's input text.

    Returns:
        tuple: A tuple in the form (intent_type, action), where:
               - intent_type (str) is either "system" or "general"
               - action (str) is the specific command or the original text
    """
    lowered = text.lower()

    # System-level intents
    if "search" in lowered and "google" in lowered:
        return "system", "googleSearch"
    elif "youtube" in lowered or ("play" in lowered and any(w in lowered for w in ["song", "video", "music"])):
        return "system", "youtube"
    elif "screenshot" in lowered or "take a screenshot" in lowered:
        return "system", "screenShot"
    elif "start word" in lowered or "open word" in lowered or "word project" in lowered:
        return "system", "startWordProject"

    # Brightness-related actions
    elif "set brightness to" in lowered and extract_number(lowered) is not None:
        return "system", "setBrightness"
    elif "brightness" in lowered and contains_any(DIM_WORDS, lowered):
        return "system", "lowerBrightness"
    elif "brightness" in lowered and contains_any(BRIGHTEN_WORDS, lowered):
        return "system", "higherBrightness"

    # Volume-related actions
    elif "set volume to" in lowered and extract_number(lowered) is not None:
        return "system", "setVolume"
    elif "volume" in lowered and contains_any(VOLUME_DOWN_WORDS, lowered):
        return "system", "lowVolume"
    elif "volume" in lowered and contains_any(VOLUME_UP_WORDS, lowered):
        return "system", "highVolume"
    elif "mute" in lowered and "volume" in lowered:
        return "system", "muteVolume"
    elif "unmute" in lowered and "volume" in lowered:
        return "system", "unmuteVolume"

    # Download music command
    elif "music" in lowered and "download" in lowered:
        return "system", "downloadMusic"

    # Fallback: general conversation or unknown commands
    else:
        return "general", text


