import yaml
import re

def parse_truth_file(content: str) -> tuple[dict, str]:
    if content.startswith("---\n"):
        parts = content.split("---\n", 2)
        if len(parts) >= 3:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
                body = parts[2]
                return metadata, body
            except yaml.YAMLError:
                pass
    return {}, content
