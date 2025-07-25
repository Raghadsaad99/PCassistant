Smart Desktop Assistant
=======================

This is a Python-based personal assistant that runs on a desktop computer. It supports both system automation and intelligent Q&A using the Gemini LLM.

----------------------------
📦 SETUP INSTRUCTIONS
----------------------------

1. Make sure Python 3.10+ is installed.

2. Install dependencies:

   pip install -r requirements.txt

3. (Optional) Set your Gemini API key as an environment variable:

   export GEMINI_API_KEY=your-api-key   # on Linux/macOS
  

   (Alternatively, the API key is hardcoded in llm_handler.py for testing.)

----------------------------
▶ HOW TO RUN
----------------------------

Run the assistant using:

   python main.py

The GUI will launch with a text field. Type a command or a question.

----------------------------
🛠 SUPPORTED COMMANDS
----------------------------

- Search Google:           "Search Python tutorials on Google"
- Search YouTube:          "Find cat videos on YouTube"
- Take a Screenshot:       "Take a screenshot"
- Control Brightness:      "Brightness up" / "Brightness down"
- Control Volume:          "Volume up" / "Volume down"
- Open MS Word:            "Start Word project"
- Download Music:          (placeholder only)
- Ask any question:        "What is a black hole?" → uses Gemini

----------------------------
💡 LLM INTEGRATION
----------------------------

- LLM Used: Gemini 2.5 Pro
- SDK: google-generativeai
- All general questions are passed to Gemini via API.

----------------------------
⚠ NOTES
----------------------------

- Brightness control is simulated.
- Volume control uses pyautogui keypress.
- LLM responses are printed directly from Gemini.
