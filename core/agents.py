# Loading the ADK:
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

# Retry-Configuration
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429,500,503,504]
)

# Log Agent Creation:
log_agent = Agent(
    name="LogAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
You extract IPs, summarize first 3 chunks, return JSON:
{
 "iocs": {"ips": []},
 "summary": "..."
}
""",
    output_key="log_result"
)

# Network Agent Creation:
network_agent = Agent(
    name="NetworkAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
Analyze JSON PCAP, extract IPs & ports, return:
{
 "iocs": {"ips": [], "ports": {}},
 "summary": "..."
}
""",
    output_key="network_result"
)

# Memory Agent Creation
memory_agent = Agent(
    name="MemoryAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="Summarize memory dump text and return IOC IPs.",
    output_key="memory_result"
)

# Aggregator Agent & Analysis Team Creation
analysis_team = ParallelAgent(
    name="ParallelTeam",
    sub_agents=[log_agent, network_agent, memory_agent],
)

aggregator_agent = Agent(
    name="CipherAggregator",
    model=Gemini(model="gemini-2.0-flash"),
    instruction="""
    You will receive outputs from log_agent, network_agent, and memory_agent.
    Combine them into a single unified security report.
    """
)

# Report Agent Creation:
report_agent = Agent(
    name="ReportAgent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="Generate a formal digital forensics report (plain text).",
    output_key="report"
)

# Root Dummy Agent:
root_agent = SequentialAgent(
    name="CipherRoot",
    sub_agents=[analysis_team, aggregator_agent, report_agent]
)