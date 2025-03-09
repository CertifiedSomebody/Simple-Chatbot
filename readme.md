
# Simple AI Chatbot 🤖

A simple AI-powered chatbot built using Python and Google Gemini API. This project demonstrates how to integrate a chatbot with voice input and text-based responses, as well as emoji support and a simple graphical user interface (GUI) built with Tkinter.

## Features

- **Text-based Chatbot**: The chatbot generates responses based on user input.
- **Voice Input**: Use your microphone to provide input to the chatbot via speech recognition.
- **Emoji Support**: Convert text into emoji with `emoji` library support.
- **Dark Mode**: Toggle between light and dark themes for the chatbot interface.
- **Chat History**: Chat history is stored in a local JSON file and persists between sessions.
- **Animated Avatar**: Display an animated chatbot avatar that changes frames as the conversation progresses.

## Requirements

- Python 3.x
- `google-generativeai` (for Google Gemini API)
- `speechrecognition` (for voice input)
- `emoji` (for emoji support)
- `Pillow` (for image processing)
- `python-dotenv` (for loading environment variables)
- Tkinter (for the GUI)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/CertifiedSomebody/Simple-Chatbot.git
   cd Simple-Chatbot
   ```

2. **Install dependencies**:
   Install the necessary Python libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Gemini API key**:
   - Create a `.env` file in the root directory of the project.
   - Add your API key in the following format:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

4. **Run the chatbot**:
   ```bash
   python chatbot_gui.py
   ```

## How It Works

- The chatbot uses Google Gemini API to generate responses based on user input.
- Voice input is captured using the SpeechRecognition library and converted to text.
- The `emoji` library is used to convert text into emojis for fun interactions.
- The Tkinter GUI provides a user-friendly interface for chatting with the bot.
- The chatbot maintains a conversation history stored in `chat_history.json` and displays it each time the app is launched.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions

Feel free to fork this project and contribute by submitting pull requests for bug fixes, features, or improvements!
