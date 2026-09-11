from dsa_study.html_tools import extract_examples, sanitize_statement


def test_sanitizer_removes_scripts_and_event_handlers():
    result = sanitize_statement('<p onclick="bad()">Keep <strong>this</strong>.</p><script>alert(1)</script>')
    assert "onclick" not in result
    assert "script" not in result
    assert "alert" not in result
    assert "<strong>this</strong>" in result


def test_extract_examples_from_common_statement_markup():
    examples = extract_examples('<p><strong>Input:</strong> nums = [2,7], target = 9</p><p><strong>Output:</strong> [0,1]</p><p><strong>Explanation:</strong> done</p>')
    assert examples == [{"input": "nums = [2,7], target = 9", "output": "[0,1]"}]
