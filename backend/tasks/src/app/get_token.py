def get_token(auth_header) -> str:
    if auth_header:
        auth_arguments = auth_header.split(" ")
        auth_name = auth_arguments[0]
        if auth_name == "Token":
            auth_token = auth_arguments[1]
        else:
            auth_token = ""
    else:
        auth_token = ""

    return auth_token
