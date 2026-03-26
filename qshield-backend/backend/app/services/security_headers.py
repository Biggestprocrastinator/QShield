import requests


def check_security_headers(domain: str) -> dict:
    try:
        response = requests.get(f"https://{domain}", timeout=5, verify=False)
        headers = {key.lower(): value for key, value in response.headers.items()}
        return {
            "hsts": "strict-transport-security" in headers,
            "csp": "content-security-policy" in headers,
            "x_frame_options": "x-frame-options" in headers,
            "x_content_type_options": "x-content-type-options" in headers,
        }
    except Exception:
        return {
            "hsts": False,
            "csp": False,
            "x_frame_options": False,
            "x_content_type_options": False,
        }
