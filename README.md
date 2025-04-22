# AI Chat Assistant

A global hotkey-triggered AI chat application that provides visual context-aware assistance using OpenAI's GPT-4o model.

## Features

- Trigger with Ctrl+Space from anywhere
- Small, semi-transparent chat window
- Visual context awareness - captures and analyzes your active window
- Uses GPT-4o for rich visual understanding
- Simple and intuitive interface

## Setup

1. Install Python 3.7 or higher
2. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Install dependencies using uv:
   ```bash
   uv pip install -e .
   ```
4. Create a `.env` file in the project directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Run the application:
   ```bash
   python -m ai_chat_assistant
   ```
   or
   ```bash
   ai-chat
   ```
2. Press Ctrl+Space anywhere to open the chat window
3. Type your message and press Enter or click Send
4. The AI will analyze your current window and provide context-aware answers
5. Click Close to hide the window (it will remain running in the background)

## Visual Context

The application automatically captures a screenshot of your active window when you send a message. This allows the AI to:
- See what you're working on
- Provide specific help about visible content
- Understand the context of your questions
- Give more accurate and relevant responses

## Cost Considerations

- Uses GPT-4o which provides excellent visual understanding
- Screenshots are automatically resized and compressed to reduce API costs
- Limited to 300 tokens per response to keep costs manageable
- Images are processed at 85% JPEG quality to reduce data size

## Security

- Your API key is stored locally in the `.env` file
- No data is stored permanently
- Screenshots are only used for the current message and not stored
- Window context is only used for the current session
