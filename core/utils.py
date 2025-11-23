import json

def combine_inputs(log_text=None, pcap_json=None, mem_text=None):
    """
    Combines log, pcap, and memory text into one unified Gemini input block.
    """
    combined = ""

    if log_text:
        combined += "[LOG]\n" + log_text + "\n\n"
    if pcap_json:
        combined += "[PCAP]\n" + json.dumps(pcap_json, indent=2) + "\n\n"
    if mem_text:
        combined += "[MEMORY]\n" + mem_text + "\n\n"

    return combined


def normalize_analysis_result(result):
    """
    Ensures result has keys: output (string), parsed (dict)
    Handles cases where ADK returns a list.
    """

    if isinstance(result, list):
        # Convert list -> dict
        return {
            "output": "\n".join([str(r) for r in result]),
            "parsed": {
                "parsed_events": [str(r) for r in result],
                "ips": [],
                "ports": {}
            }
        }

    # Ensure parsed is dictionary
    parsed = result.get("parsed", {})
    if isinstance(parsed, list):
        parsed = {"parsed_events": [str(x) for x in parsed]}
    result["parsed"] = parsed

    return result