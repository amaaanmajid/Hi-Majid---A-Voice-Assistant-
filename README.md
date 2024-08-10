## Description

"Hi Majid!" Chatbot is a voice-activated AI assistant that interacts with users through speech recognition and text-to-speech. It offers real-time responses, weather updates, and personalized greetings based on the time of day.

## Personalized Features

- **Voice Interaction**: Speak to the chatbot, and it will respond with synthesized speech.
- **Weather Information**: Get current weather updates for any city.
- **Personalized Greeting**: Provides greetings based on the time of day and user interaction.

## Demo 

![Chatbot Demo](voice%20chatbot%20demo.JPG)

## Building

### Requirements

* `ollama`: For integrating with the LLaMA model.
* `speech_recognition`: For converting speech to text.
* `gtts`: For converting text to speech using Google Text-to-Speech.
* `pygame`: For playing audio files.
* `requests`: For making HTTP requests to the OpenWeatherMap API.
* Python: Version 3.7 or higher
* Git: For version control and cloning the repository.

### Basic Work-Flow
                        


1. **Initialization**:
   - The chatbot initializes various components, including the microphone, audio queues, and threading events.
   - Sets up hotkey listeners and prepares for interaction.

2. **Listening**:
   - The chatbot listens for voice input through the microphone.
   - The speech is converted to text using the `speech_recognition` library.

3. **Trigger Detection**:
   - The chatbot detects if the user has mentioned the trigger word ("Majid").
   - If the trigger word is detected, it processes the subsequent voice command.

4. **Command Processing**:
   - The chatbot identifies the command or request:
     - **Greeting**: If no specific request is made, it greets the user.
     - **Name Inquiry**: Responds with the chatbot’s name if asked.
     - **Weather Inquiry**: Extracts the city from the request and fetches weather information using the OpenWeatherMap API.
     - **General Conversation**: Processes the text through the LLaMA model for generating responses.

5. **Text-to-Speech Conversion**:
   - Converts the generated text response into speech using the `gtts` library.
   - Queues the audio data for playback.

6. **Playing Audio**:
   - Plays the generated audio response through the speakers using the `pygame` library.

7. **Logging**:
   - Logs interactions and responses to a text file for record-keeping.

8. **Handling Special Cases**:
   - Handles specific commands like "That's all" to end the conversation and put the chatbot back into listening mode.

9. **Repetition**:
   - Continues listening and processing commands in a loop until stopped.

### Installing Required and Optional Dependencies

To install the required dependencies, create a `requirements.txt` file with the following content:

```bash
pip install -r requirements.txt
