from app.get_token import get_token


def test_get_token():
    auth_header = "Token 11111"
    token = get_token(auth_header)
    assert token == "11111"
