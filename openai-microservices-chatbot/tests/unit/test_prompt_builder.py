import pytest
from services.ai_inference_service.main import build_prompt

def test_build_prompt_empty_history():
    messages = build_prompt([], "Hello!")
    assert messages[0]["role"] == "system"
    assert messages[-1]["role"] == "user"
    assert messages[-1]["content"] == "Hello!"

def test_build_prompt_with_history():
    history = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"}
    ]
    messages = build_prompt(history, "How are you?")
    assert len(messages) == 4
    assert messages[-1]["content"] == "How are you?"

def test_build_prompt_sliding_window():
    """Verify only last 10 messages are kept."""
    history = [{"role": "user", "content": f"msg {i}"} for i in range(20)]
    messages = build_prompt(history, "new message")
    assert len(messages) <= 12  # system + 10 history + 1 new
