# Simple Agent

A toy example of how absurdly easy it is to write a working agent. I wrote this to highlight a few things that are easy to miss when you only interact with LLMs through polished UIs. The core architecture is smaller than this README. 

At the core, every agent is just:

1. **An LLM**
2. **A loop**
3. **Some tools the model can call**
4. **Context**

### Agents aren't complex because the model handles everything

- deciding when to act  
- calling tools  
- fixing arguments  
- retrying  
- planning  
- analyzing results  
- deciding when to stop

### Tool Use is a software engineering holy shit moment worth implementing

You hand the model a list of functions:

- `ping`
- `curl`
- `ascii_art`
- anything else you expose

The LLM chooses when to call them and what parameters to use. If a tool returns something unexpected, it tries another approach. The LLM does the reasoning, orchestration, and reflects on its own.

### Spend an extra month and build your own agentic IDE

Toss in a few tools and `subprocess` + `stdin` + `stdout` takes care of the rest:
- `read_file`
- `write_file`
- `run`
- `test`
- `search`
- `refactor`

You don't even need to fork VS Code, just run it on your terminal.

### LLMs Don’t “Remember” Anything. 

They’re stateless. All their memory lives in the loop that feeds from the prior message + reasoning context. The agent *feels* stateful only because you keep resending the entire conversation back to the model.

## Features

- Interactive conversation with GPT-5
- Tools:
  - `ping`: Ping hosts to check connectivity
  - `curl`: Execute curl commands to validate HTTPS or fetch headers
  - `ascii`: Generate simple ascii art
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

```bash
python simple_agent.py
```

The agent will process your input and can execute tools as needed. For example, you can ask it to:
- Ping a host: Ping google.com
- Check HTTPS headers: "Check the headers for https://example.com
- Create simple ascii art 

You can also use standard assistant output as the script preserves the reasoning contract.
- tell me a joke

## How It Works

1. The agent maintains a conversation context that includes user messages, assistant responses, and tool call results.
2. When you provide input, the agent sends it to GPT-5 along with available tools.
3. If GPT-5 decides to use a tool, the agent executes it and adds the results back to the context.
4. The process continues until GPT-5 provides a final response without tool calls.
5. The final response is displayed to the user.


