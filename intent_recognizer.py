def recognize_intent(text: str) -> tuple:
    lowered = text.lower()

    if "search" in lowered and "google" in lowered:
        return "system", "googleSearch"
    
    elif "youtube" in text.lower() or "play" in text.lower():
        return "system", "youtube"
    elif "screenshot" in lowered:
        return "system", "screenShot"
    elif "start word" in lowered or "word" in lowered:
        return "system", "startWordProject"
    elif "brightness" in lowered and "lower" in lowered:
        return "system", "lowerBrightness"
    elif "brightness" in lowered and "higher" in lowered:
        return "system", "higherBrightness"
    elif "volume" in lowered and "low" in lowered:
        return "system", "lowVolume"
    elif "volume" in lowered and "high" in lowered:
        return "system", "highVolume"
    elif "music" in lowered and "download" in lowered:
        return "system", "downloadMusic"
    else:
        return "general", text
