def mock_llm_response(query):
    return "This is a test response"

def test_llm_response():
    response = mock_llm_response("Check balance")
    assert response is not None
    assert isinstance(response, str)
