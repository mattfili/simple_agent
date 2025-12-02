# Simple Agent

A simple command-line agent that uses OpenAI's GPT-5 model to interact with users and execute network tools like `ping` and `curl`. The agent maintains conversation context and can make function calls to perform network diagnostics.

## Features

- Interactive conversation with GPT-5
- Network tools:
  - `ping`: Ping hosts to check connectivity
  - `curl`: Execute curl commands to validate HTTPS or fetch headers
- Conversation context management
- Function calling with automatic tool execution

## Requirements

- Python 3.10 or higher
- OpenAI API key
- `uv` package manager (or pip)

## Setup

1. Install dependencies using `uv`:
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key in `simple_agent.py`:
   - Open `simple_agent.py`
   - Replace the empty string on line 6 with your API key:
   ```python
   client = OpenAI(api_key="your-api-key-here")
   ```

## Usage

The agent provides a `process()` function that takes user input and returns the assistant's response. To run interactively, you can add a main loop to `simple_agent.py`:

```python
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        process(user_input)
```

Then run:
```bash
python -i simple_agent.py
```

The agent will process your input and can execute network tools as needed. For example, you can ask it to:
- `process("Ping a host: Ping google.com)`
- `process("Check HTTPS headers: "Check the headers for https://example.com)")`

You can also use standard assistant output as the script preserves the reasoning contract.
- process("tell me a joke")

## How It Works

1. The agent maintains a conversation context that includes user messages, assistant responses, and tool call results.
2. When you provide input, the agent sends it to GPT-5 along with available tools.
3. If GPT-5 decides to use a tool, the agent executes it and adds the results back to the context.
4. The process continues until GPT-5 provides a final response without tool calls.
5. The final response is displayed to the user.

## Tools

### ping
Pings a host to check network connectivity.
- Parameters: `host` (hostname or IP address)

### curl
Executes curl commands locally to validate HTTPS or fetch headers.
- Parameters: `args` (array of curl arguments)

## Notes

- The agent uses OpenAI's `responses.create()` API endpoint with the `gpt-5` model.
- All tool executions are logged to the console for debugging purposes.
- The conversation context persists throughout the session.

