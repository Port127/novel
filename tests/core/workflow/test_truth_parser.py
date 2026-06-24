import pytest
from novel.core.workflow.truth_parser import parse_truth_file

def test_parse_truth_file():
    content = "---\nname: 陈汉升\nstatus: alive\n---\n# 陈汉升\n主角，渣男。"
    metadata, body = parse_truth_file(content)
    assert metadata == {"name": "陈汉升", "status": "alive"}
    assert body.strip() == "# 陈汉升\n主角，渣男。"

def test_parse_truth_file_no_frontmatter():
    content = "# 简单文本\n无 Metadata。"
    metadata, body = parse_truth_file(content)
    assert metadata == {}
    assert body.strip() == "# 简单文本\n无 Metadata。"
