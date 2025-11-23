from google.adk.runners import InMemoryRunner
from .agents import root_agent

runner = InMemoryRunner(agent=root_agent)

async def run_cipher_ai_async(log_text=None, pcap_json=None, mem_text=None):

    import json

    combined = ""

    if log_text:
        combined += "[LOG]\n" + log_text + "\n\n"

    if pcap_json:
        combined += "[PCAP]\n" + json.dumps(pcap_json, indent=2) + "\n\n"

    if mem_text:
        combined += "[MEMORY]\n" + mem_text + "\n\n"

    # run_debug EXPECTS: list[str]
    return await runner.run_debug([combined])