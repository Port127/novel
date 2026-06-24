import yaml
import re

def parse_truth_file(content: str) -> tuple[dict, str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    
    if match:
        yaml_content = match.group(1)
        body = content[match.end():]
        
        try:
            metadata = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter: {e}")
            
        if metadata is None:
            metadata = {}
        elif not isinstance(metadata, dict):
            raise ValueError("YAML frontmatter must be a dictionary")
            
        return metadata, body
        
    return {}, content
