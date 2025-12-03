import json
import subprocess
from openai import OpenAI

client = OpenAI(api_key="")
context = []

tools = [
    {
        "type": "function",
        "name": "ping",
        "description": "ping a host",
        "parameters": {
            "type": "object",
            "properties": {"host": {"type": "string"}},
            "required": ["host"]
        }
    },
    {
        "type": "function",
        "name": "curl",
        "description": "run curl with arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "args": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["args"]
        }
    },
    {
        "type": "function",
        "name": "ascii_art",
        "description": "Render text as simple ASCII art banner for terminal display",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to render as ASCII art"
                }
            },
            "required": ["text"]
        }
    }
]

def log(msg):
    print(f"[LOG] {msg}")

def ping(host):
    result = subprocess.run(
        ["ping", "-c", "2", host],
        text=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
    )
    return result.stdout

def curl(args):
    result = subprocess.run(
        ["curl"] + args,
        text=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE
    )
    return result.stdout

def ascii_art(text: str) -> str:
    line = "#" * (len(text) + 4)
    return f"{line}\n# {text} #\n{line}\n"

def call_model():
    return client.responses.create(
        model="gpt-5",
        tools=tools,
        input=context
    )

TOOL_REGISTRY = {
    "ping": ping,
    "curl": curl,
    "ascii_art": ascii_art,
}

def tool_call(fc_item):
    name = fc_item.name
    args = json.loads(fc_item.arguments)

    tool_func = TOOL_REGISTRY.get(name, lambda _: "unknown tool")
    out = tool_func(**args)

    return {
        "type": "function_call_output",
        "call_id": fc_item.call_id,
        "output": out
    }

def handle_output(response):
    updated = False
    pending_reasoning = None

    for item in response.output:

        if item.type == "reasoning":
            pending_reasoning = item
            continue

        if pending_reasoning:
            context.append(pending_reasoning)
            pending_reasoning = None

        if item.type == "function_call":
            log(f"Function call: {item.name} {json.loads(item.arguments)}")
            fc_out = tool_call(item)
            context.extend([item, fc_out])
            updated = True
            continue

        context.append(item)

    return updated

def process(user_input):
    context.append({"role": "user", "content": user_input})

    response = call_model()

    while handle_output(response):
        response = call_model()

    context.append({"role": "assistant", "content": response.output_text})

    print("\n=== ASSISTANT ===")
    return print(response.output_text)
    print("=================\n")

if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        process(user_input)
