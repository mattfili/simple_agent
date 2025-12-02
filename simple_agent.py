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

def call_model():
    return client.responses.create(
        model="gpt-5",
        tools=tools,
        input=context
    )

def tool_call(fc_item):
    name = fc_item.name
    args = json.loads(fc_item.arguments)

    if name == "ping":
        out = ping(**args)
    elif name == "curl":
        out = curl(**args)
    else:
        out = "unknown tool"

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
            log(f"Reasoning:\n{item}\n")
            pending_reasoning = item
            continue

        # If there was reasoning, append it before this item
        if pending_reasoning:
            context.append(pending_reasoning)
            pending_reasoning = None

        if item.type == "function_call":
            log(f"Function call: {item.name}")
            fc_out = tool_call(item)
            context.extend([item, fc_out])
            updated = True
            continue

        # Normal assistant message/output_text
        context.append(item)

    return updated

def process(user_input):
    log(f"User: {user_input}")
    context.append({"role": "user", "content": user_input})

    response = call_model()

    # Keep looping while tool calls happen
    while handle_output(response):
        response = call_model()


    # Store final text as assistant message
    context.append({"role": "assistant", "content": response.output_text})

    print("\n=== ASSISTANT ===")
    return print(response.output_text)
    print("=================\n")
