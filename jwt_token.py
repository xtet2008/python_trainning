import base64
import json
from datetime import datetime
import jwt  # requires PyJWT package


def decode_jwt_without_verification(token):
    """
    Decode a JWT token without verifying the signature.
    Useful for inspecting token contents.
    """
    # Split the token into parts
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    # Decode the header and payload
    header = base64_url_decode(parts[0])
    payload = base64_url_decode(parts[1])

    # Parse JSON
    header_data = json.loads(header)
    payload_data = json.loads(payload)

    # Format timestamps
    if 'iat' in payload_data:
        payload_data['iat_formatted'] = datetime.fromtimestamp(
            payload_data['iat']).strftime('%Y-%m-%d %H:%M:%S UTC')
    if 'exp' in payload_data:
        payload_data['exp_formatted'] = datetime.fromtimestamp(
            payload_data['exp']).strftime('%Y-%m-%d %H:%M:%S UTC')
    if 'auth_time' in payload_data:
        payload_data['auth_time_formatted'] = datetime.fromtimestamp(
            payload_data['auth_time']).strftime('%Y-%m-%d %H:%M:%S UTC')

    return {
        'header': header_data,
        'payload': payload_data
    }


def base64_url_decode(input):
    """Decode base64url-encoded string"""
    # Add padding if needed
    remainder = len(input) % 4
    if remainder > 0:
        input += '=' * (4 - remainder)

    # Replace URL-safe characters
    input = input.replace('-', '+').replace('_', '/')

    # Decode
    return base64.b64decode(input).decode('utf-8')


def verify_cognito_token(token, region=None, user_pool_id=None):
    """
    Verify a Cognito JWT token.
    For full verification, needs AWS credentials or public key.
    """
    try:
        # For demonstration only - in production, you'd use the actual key
        # This will NOT verify the signature, just decode
        decoded = jwt.decode(
            token,
            options={"verify_signature": False}  # Skip signature verification
        )
        return {
            "valid": "Unknown (signature not verified)",
            "decoded": decoded
        }
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token has expired"}
    except jwt.InvalidTokenError as e:
        return {"valid": False, "error": str(e)}


# Example usage
if __name__ == "__main__":
    # The token to analyze
    token = "eyJraWQiOiJHaHQrTmV4VkNDdHl5Ykc3b0ZpZHVVZFROYUFsWENCK2Q0V3ZqUGNsaTdzPSIsImFsZyI6IlJTMjU2In0.eyJjdXN0b206Y291bnRyeSI6IkNoaW5hIiwic3ViIjoiNDQ0ODE0NDgtMDA1MS03MGI4LWVjYzQtOWI3ZTk1NGU5MTZjIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX3lvdktVRXdkcCIsImNvZ25pdG86dXNlcm5hbWUiOiI0NDQ4MTQ0OC0wMDUxLTcwYjgtZWNjNC05YjdlOTU0ZTkxNmMiLCJvcmlnaW5fanRpIjoiODhkMGRiOTItYTM1Ni00NmE2LWEyZWYtZTU0ZmI4ZTVhZGRlIiwiYXVkIjoiMjUwMGg4ZWwyZnNpcjhmNWdycTk3aDY1YmgiLCJldmVudF9pZCI6ImZiMTU2NGE1LTVlZDctNGU5Yi05ZTRjLTAxMGNkMWNmYmI2MiIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzQ5NzIxNDc5LCJuYW1lIjoieHRldDIwMDgiLCJleHAiOjE3NDk4MDc4NzksImlhdCI6MTc0OTcyMTQ3OSwianRpIjoiYzg3MmY0ODQtZTNlOC00Mjk2LTk3OWYtNjU5MDlmMTI4OGM1IiwiZW1haWwiOiJ4dGV0MjAwOEAxMjYuY29tIn0.ir4ATlANBOOerNA3eyFt0y2H5psmeUfmtUORkZ_iOrYcptjVqOrdBQkzYEuXbKIC5aab_69-jBNnznZsS2b46kVSAd99msaoZHWhnB3VmpY7ZWnfgqdSpaUjz5T1DXjQhRHWXFrxls20m1FBXE6dqXGvSTfekiFU2l4psMYYEIolEoZjQBBcvETfjb-LRZeOhJnOwhekLqwFidx5GRCaAv1_hwbEFS4Mnn3ZUUPuvFvCVFvCkMNmB4c6qyjJN_uFXf5C4P_I8FwTjIoPfQwVdTo2Nx0_k3PkSz5UHH5iAY_kA7r4eY3XiZpcXg-O4wqxfA0FYC5ZjfokCDn21i9D-A"

    # Simple decoding without verification
    decoded_token = decode_jwt_without_verification(token)
    print("Header:")
    print(json.dumps(decoded_token['header'], indent=2))
    print("\nPayload:")
    print(json.dumps(decoded_token['payload'], indent=2))

    # Verification (will only work partially without the actual key)
    verification_result = verify_cognito_token(token)
    print("\nVerification result:")
    print(verification_result['valid'])
