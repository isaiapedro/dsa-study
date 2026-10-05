from dsa_study.learning_blocks import load_learning_blocks, select_catalog_practice


def test_initial_learning_blocks_meet_authoring_contract():
    blocks = load_learning_blocks()

    assert [block["id"] for block in blocks] == [
        "arrays-indexing-contracts",
        "hashing-collision-reasoning",
        "two-pointers-monotonic-movement",
        "binary-search-interval-invariant",
        "linked-lists-rewiring-contracts",
        "stacks-queues-order-contracts",
        "trees-recursive-return-contracts",
        "bfs-dfs-frontier-visited-contracts",
        "dynamic-programming-dependency-contracts",
    ]
    for block in blocks:
        assert block["duration_minutes"] == 45
        assert block["tool_time_ceiling_minutes"] == 8
        assert set(block["outcomes"]) == {
            "foundation",
            "interview",
            "professional_transfer",
        }
        assert {question["kind"] for question in block["questions"]} == {
            "retrieval",
            "invariant",
            "next-state",
            "contrast",
            "invalid-use",
        }
        assert len(block["questions"]) == 5
        assert block["question_provenance"] == "project-authored-review-required"
        assert {prompt["lens"] for prompt in block["pre_code_checkpoint"]["prompts"]} == {
            "input_output", "constraint", "state_invariant", "selection",
        }
        assert block["curriculum_context"]["part_of"]
        assert block["curriculum_context"]["selection_dimensions"]
        assert block["visual"]["required_controls"] == ["play", "pause", "step", "reset"]
        assert len(block["visual"]["states"]) >= 3
        assert block["faded_scaffold"]["pseudocode"]
        assert block["independent_practice"]["stop_rule"]
        assert block["feedback_checklist"]
        practice = block["catalog_practice"]
        assert practice["technique"]
        assert practice["required_topic_slugs"]
        assert practice["constraints"]
        assert [prompt["label"] for prompt in block["interview_prompts"]] == [
            "Approach", "Correctness", "Complexity", "Boundary test", "Contrast",
        ]


def test_catalog_practice_uses_declared_required_and_preferred_topic_rules():
    block = next(block for block in load_learning_blocks() if block["id"] == "two-pointers-monotonic-movement")
    problems = [
        {"id": "3", "slug": "array-only", "topics": [{"slug": "array"}]},
        {"id": "2", "slug": "two-pointer", "topics": [{"slug": "array"}, {"slug": "two-pointers"}]},
        {"id": "1", "slug": "hash-only", "topics": [{"slug": "hash-table"}]},
    ]

    assert [problem["slug"] for problem in select_catalog_practice(block, problems)] == [
        "two-pointer", "array-only",
    ]
