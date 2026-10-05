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


def test_extract_examples_stops_before_the_next_example_heading():
    markup = "<p>Example 1:</p><p>Input: nums = [2,7], target = 9 Output: [0,1]</p><p>Example 2:</p><p>Input: nums = [3,2,4], target = 6 Output: [1,2]</p>"
    assert extract_examples(markup) == [
        {"input": "nums = [2,7], target = 9", "output": "[0,1]"},
        {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"},
    ]
