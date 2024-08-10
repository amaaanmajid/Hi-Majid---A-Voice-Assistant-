# Hi-Majid-A-Voice-Assistant-
A LLama-3 based voice-activated chatbot that provides weather updates, personalized greetings, and interactive responses using real-time speech recognition and text-to-speech.
Hi Majid Chatbot is a voice-activated AI assistant designed to provide information and interact with users through speech recognition and text-to-speech capabilities. It features real-time responses, weather updates, and personalized greetings.

Features-
Voice Interaction: Speak to the chatbot, and it will respond with synthesized speech.
Weather Information: Get current weather updates for any city.
Personalized Greeting: Receives and processes commands, providing greetings based on the time of day.

Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/your-repo-name.git
Navigate to the Project Directory:

bash
Copy code
cd your-repo-name
Install Required Packages:
Ensure you have Python 3.7+ installed. Create a virtual environment and install dependencies:

bash
Copy code
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
pip install -r requirements.txt
Usage
Run the Chatbot:

bash
Copy code
python main.py
Interact with the Bot:

Speak to the bot using a microphone.
Activate the bot by saying 'Hi Majid'. It will greet you back based on the specific time of the day(Good Morning/ Good evening etc.)
Use commands like "weather in [city]" to get weather updates.
Ask "What's your name?" or say "That's all" to end the interaction.
Configuration
API Key:
Replace the placeholder API key in main.py with your own OpenWeatherMap API key to get weather information.
Update api_key variable in get_weather function.
Contributing
Feel free to submit pull requests or open issues if you have suggestions or encounter problems. Contributions are welcome!


