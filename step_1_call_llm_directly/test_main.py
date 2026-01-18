from unittest.mock import Mock, patch
import pytest
from step_1_call_llm_directly.main import LlmClient


@pytest.fixture
def mock_llm():
    """Fixture that provides a mocked ChatAnthropic instance"""
    with patch('step_1_call_llm_directly.main.ChatAnthropic') as mock_llm_class:
        mock_llm_instance = Mock()
        mock_llm_class.return_value = mock_llm_instance
        yield mock_llm_instance, mock_llm_class


def test_invoke_llm_simple_prompt_it_should_invoke_llm_and_return_response(mock_llm):
    # Arrange: Setup mock response
    mock_llm_instance, mock_llm_class = mock_llm
    mock_response = Mock()
    mock_response.content = "Paris"
    mock_llm_instance.invoke.return_value = mock_response
    
    # Act
    user_prompt = "What is the capital of France?"
    llm_client = LlmClient()
    response = llm_client.invoke(user_prompt)
    
    # Assert
    assert response.content == "Paris"
    mock_llm_instance.invoke.assert_called_once_with(user_prompt)
    mock_llm_class.assert_called_once_with(model="claude-3-haiku-20240307", temperature=0)


def test_invoke_llm_with_different_response(mock_llm):
    """Test with a different scenario to ensure mocking works properly"""
    # Arrange
    mock_llm_instance, _ = mock_llm
    mock_response = Mock()
    mock_response.content = "The capital of France is Paris."
    mock_llm_instance.invoke.return_value = mock_response
    
    # Act
    llm_client = LlmClient()
    response = llm_client.invoke("Tell me about Paris")
    
    # Assert
    assert response.content == "The capital of France is Paris."
    mock_llm_instance.invoke.assert_called_once()
    