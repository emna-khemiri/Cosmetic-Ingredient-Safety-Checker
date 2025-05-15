from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from config import load_config
from data_loader import load_cosing_data
from chromadb_manager import ChromaDBManager
from safety_checker import SafetyChecker
from prompt_builder import build_prompt

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Simplify for local testing
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load config
config = load_config()

class IngredientQuery(BaseModel):
    name: str

@app.post("/check")
async def check_ingredient(query: IngredientQuery):
    try:
        json_files = load_cosing_data(config["data_dir"])
        chromadb_manager = ChromaDBManager(config["collection_name"])
        chromadb_manager.populate(json_files)
        safety_checker = SafetyChecker(config["api_key"], chromadb_manager)
        
        retrieved_info = chromadb_manager.query(query.name, top_k=3)
        prompt = build_prompt(query.name, retrieved_info)
        response = safety_checker.model.generate_content(prompt, stream=False)
        return {"ingredient": query.name, "safety_info": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Cosmetic Ingredient Safety Checker API"}