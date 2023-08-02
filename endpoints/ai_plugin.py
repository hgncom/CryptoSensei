from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

@router.get("/ai-plugin.json")
def ai_plugin():
    try:
        file_path = os.path.join(os.path.dirname(__file__), "ai-plugin.json")

        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="ai-plugin.json not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")