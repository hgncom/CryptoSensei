from fastapi import HTTPException

class ExternalAPIError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=503, detail=detail)

class APIResponseError(HTTPException):
    def __init__(self, message: str = "Error in API response."):
        super().__init__(status_code=502, detail=message)

class JSONDecodeError(HTTPException):
    def __init__(self, message: str = "Error decoding data from the external API."):
        super().__init__(status_code=502, detail=message)

class InvalidCryptoSymbol(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="The requested cryptocurrency symbol was not found.")
