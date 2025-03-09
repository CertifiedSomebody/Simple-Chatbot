import os
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, PhotoImage
from dotenv import load_dotenv
import google.generativeai as genai
import speech_recognition as sr
import emoji
from PIL import Image, ImageTk

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    messagebox.showerror("Error", "API key not found. Make sure it's set in the .env file.")
    exit()

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Chat history file
CHAT_HISTORY_FILE = "chat_history.json"

# Load chat history
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
                return [msg for msg in json.load(file) if "content" in msg]
        except json.JSONDecodeError:
            return []
    return []

# Save chat history
def save_chat_history():
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, indent=4)

# Generate response
def chatbot_response(user_input):
    global chat_history

    chat_history.append({"role": "user", "content": user_input})

    try:
        response = model.generate_content(user_input)
        bot_reply = response.text.strip() if response else "Sorry, I couldn't generate a response."
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    chat_history.append({"role": "bot", "content": bot_reply})
    save_chat_history()
    return bot_reply

# Convert avatar images to PNG if needed
def convert_images():
    input_folder = "avatar/"
    output_folder = "avatar_converted/"
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".jpeg", ".webp")):  # Convert JPG/WEBP to PNG
            img = Image.open(os.path.join(input_folder, filename))
            new_filename = os.path.splitext(filename)[0] + ".png"
            img.save(os.path.join(output_folder, new_filename), "PNG")

# Convert images before loading
convert_images()

# GUI Setup
root = tk.Tk()
root.title("AI Chatbot 🤖")
root.geometry("550x700")
root.configure(bg="#f0f0f0")

# Chat history
chat_history = load_chat_history()

# Dark Mode Toggle
dark_mode = False

# Toggle Theme
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    root.configure(bg="#1e1e1e" if dark_mode else "#f0f0f0")
    chat_display.configure(bg="#2e2e2e" if dark_mode else "white", fg="white" if dark_mode else "black")
    entry_box.configure(bg="#3e3e3e" if dark_mode else "white", fg="white" if dark_mode else "black")
    
    for button in [send_button, clear_button, toggle_button, voice_button]:
        button.configure(bg="#444" if dark_mode else "lightgray", fg="white" if dark_mode else "black")

# Scrollable Chat Display with Chat Bubbles (Fix Alignment)
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 12), padx=10, pady=10)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)  # ✅ Fixed layout issue
chat_display.config(state=tk.DISABLED)

# Define styles for chat bubbles
chat_display.tag_configure("user_message", justify="right", font=("Arial", 12, "bold"), foreground="blue")
chat_display.tag_configure("bot_message", justify="left", font=("Arial", 12), foreground="green")

# Display previous chat history
def display_chat_history():
    chat_display.config(state=tk.NORMAL)
    chat_display.delete(1.0, tk.END)
    for message in chat_history:
        if "content" not in message:
            continue
        role = "You" if message["role"] == "user" else "Chatbot"
        tag = "user_message" if message["role"] == "user" else "bot_message"
        chat_display.insert(tk.END, f"{role}: {message['content']}\n\n", tag)
    chat_display.config(state=tk.DISABLED)

display_chat_history()

# Send message function
def send_message():
    user_input = entry_box.get("1.0", tk.END).strip()
    if not user_input:
        return

    entry_box.delete("1.0", tk.END)
    user_input = emoji.emojize(user_input, language="alias")  # Convert text to emoji
    
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_input}\n\n", "user_message")

    bot_response = chatbot_response(user_input)

    chat_display.insert(tk.END, f"Chatbot: {bot_response}\n\n", "bot_message")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

# Clear chat history
def clear_chat():
    global chat_history
    chat_history = []
    save_chat_history()
    chat_display.config(state=tk.NORMAL)
    chat_display.delete(1.0, tk.END)
    chat_display.config(state=tk.DISABLED)

# Speech Recognition (Voice Input)
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            status_label.config(text="Listening... 🎤")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            entry_box.insert(tk.END, text)
            status_label.config(text="Voice Input Ready 🎙️")
        except sr.UnknownValueError:
            status_label.config(text="Could not understand audio ❌")
        except sr.RequestError:
            status_label.config(text="Speech recognition service unavailable 🚫")

# Load chatbot avatar images (Animated)
avatar_folder = "avatar_converted/"
avatar_images = [ImageTk.PhotoImage(Image.open(f"{avatar_folder}frame{i}.png").resize((80, 80))) for i in range(1, 4)]

# ✅ Proper Avatar Frame Placement
avatar_frame = tk.Frame(root, bg="#f0f0f0")
avatar_frame.pack(pady=5)

avatar_label = tk.Label(avatar_frame, bg="#f0f0f0")
avatar_label.pack()

# Animate avatar properly
def animate_avatar(frame=0):
    avatar_label.config(image=avatar_images[frame])
    root.after(500, animate_avatar, (frame + 1) % len(avatar_images))  # Cycle through images every 500ms

# Start animation
animate_avatar()

# Input Box
entry_box = tk.Text(root, height=3, font=("Arial", 12))
entry_box.pack(padx=10, pady=5, fill=tk.X)

# ✅ Proper Button Frame Alignment
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=5, fill=tk.X)

send_button = tk.Button(button_frame, text="Send", command=send_message, bg="lightgray", font=("Arial", 12, "bold"))
send_button.pack(side=tk.LEFT, padx=5)

voice_button = tk.Button(button_frame, text="🎤 Voice", command=recognize_speech, bg="lightgray", font=("Arial", 12, "bold"))
voice_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear Chat", command=clear_chat, bg="lightgray", font=("Arial", 12, "bold"))
clear_button.pack(side=tk.LEFT, padx=5)

toggle_button = tk.Button(button_frame, text="Dark Mode", command=toggle_theme, bg="lightgray", font=("Arial", 12, "bold"))
toggle_button.pack(side=tk.LEFT, padx=5)

# Status Label
status_label = tk.Label(root, text="Voice Input Ready 🎙️", bg="#f0f0f0", font=("Arial", 10))
status_label.pack(pady=5)

# Run GUI
root.mainloop()