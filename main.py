import tkinter as tk
from tkinter import scrolledtext, font
from intent_recognizer import recognize_intent
from automation import execute_command
from llm_handler import ask_llm

def submit_command(event=None):
    user_input = input_field.get().strip()
    if not user_input or user_input == placeholder:
        return

    log_area.insert(tk.END, f"User: {user_input}\n")
    log_area.see(tk.END)

    intent_type, action = recognize_intent(user_input)
    output_area.config(state='normal')

    if intent_type == "system":
        result = execute_command(action, user_input)
        
        
    else:
        result = ask_llm(user_input)

    if result is None:
        result = "[No response from LLM]"
    output_area.insert(tk.END, result + "\n\n")
    output_area.see(tk.END)
    output_area.config(state='disabled')

    input_field.delete(0, tk.END)
    input_field.focus()

# GUI setup
root = tk.Tk()
root.title("Smart Desktop Assistant")
root.geometry("700x500")
root.configure(bg="#f7f9fc")

header_font = font.Font(family="Helvetica", size=18, weight="bold")
text_font = font.Font(family="Arial", size=12)

tk.Label(root, text="Smart Desktop Assistant",
         font=header_font, fg="#0a2351", bg="#f7f9fc").pack(pady=(15, 10))

input_frame = tk.Frame(root, bg="#f7f9fc")
input_frame.pack(padx=10, pady=10, fill='x')

placeholder = "Type your command or question here..."
input_field = tk.Entry(input_frame, font=text_font, fg="gray")
input_field.insert(0, placeholder)
input_field.pack(side="left", fill='x', expand=True, padx=(0, 10))

def on_focus_in(e):
    if input_field.get() == placeholder:
        input_field.delete(0, tk.END)
        input_field.config(fg="black")

def on_focus_out(e):
    if not input_field.get():
        input_field.insert(0, placeholder)
        input_field.config(fg="gray")

input_field.bind("<FocusIn>", on_focus_in)
input_field.bind("<FocusOut>", on_focus_out)

tk.Button(input_frame, text="Submit", command=submit_command,
          bg="#ceddf2", fg="black",
          font=("Helvetica", 12, "bold"),
          activebackground="#aacbe9", relief="flat",
          padx=15, pady=5).pack(side="right")

output_area = scrolledtext.ScrolledText(root, font=text_font,
                                        bg="white", fg="black",
                                        state='disabled', height=12, wrap=tk.WORD)
output_area.pack(padx=10, pady=(0, 5), fill='both', expand=True)

log_area = scrolledtext.ScrolledText(root, font=("Courier New", 10),
                                     bg="white", fg="black",
                                     height=6, wrap=tk.WORD)
log_area.pack(padx=10, pady=(0, 10), fill='both', expand=True)

root.bind('<Return>', submit_command)
input_field.focus()

root.mainloop()

