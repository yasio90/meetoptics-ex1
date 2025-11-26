from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from gemini_service import GeminiServiceError


client = TestClient(app)


def test_read_root():
    """Test the root endpoint to ensure the API is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Summarizer API is running."}


# The @patch decorator intercepts the call to 'get_summary_from_gemini'
# within the 'main' module, where it's being imported and used.
@patch('main.get_summary_from_gemini')
def test_summarize_endpoint_success(mock_get_summary):
    """Test the /summarize endpoint for a successful scenario."""
    
    mock_summary = "This is a mock summary."
    mock_get_summary.return_value = mock_summary

    test_text = "This is a long piece of text to be summarized."
    
    response = client.post("/summarize", json={"text": test_text})

    assert response.status_code == 200
    assert response.json() == {"summary": mock_summary}
    
    mock_get_summary.assert_called_once_with(test_text)


@patch('main.get_summary_from_gemini')
def test_summarize_endpoint_service_error(mock_get_summary):
    """Test how the /summarize endpoint handles a specific GeminiServiceError."""
    
    error_message = "API connection failed"
    mock_get_summary.side_effect = GeminiServiceError(error_message)

    response = client.post("/summarize", json={"text": "Some text."})

    assert response.status_code == 503
    assert response.json()["detail"] == error_message


def test_summarize_endpoint_empty_text():
    """Test that Pydantic validation rejects empty or whitespace-only strings."""
    
    response = client.post("/summarize", json={"text": "   "})

    # Assert that the request was rejected with the correct status code
    # for a validation error.
    assert response.status_code == 422
    assert "detail" in response.json()
