from config import load_config
from data_loader import load_cosing_data
from chromadb_manager import ChromaDBManager
from safety_checker import SafetyChecker

def main():
    """Main application for cosmetic ingredient safety checker."""
    print("🔬 Cosmetic Ingredient Safety Checker (EU Regulations with ChromaDB RAG)")
    
    # Load configuration
    config = load_config()
    
    # Load COSING data
    json_files = load_cosing_data(config["data_dir"])
    
    # Initialize ChromaDB
    chromadb_manager = ChromaDBManager(config["collection_name"])
    chromadb_manager.populate(json_files)
    
    # Initialize safety checker
    safety_checker = SafetyChecker(config["api_key"], chromadb_manager)
    
    # Main loop
    print("Enter ingredient names to check their safety status. Type 'quit' to exit.\n")
    while True:
        query = input("💡 Enter ingredient name (or 'quit' to exit): ").strip()
        if query.lower() == "quit":
            print("Exiting...")
            break
        if not query:
            print("Please enter a valid ingredient name.")
            continue
        safety_checker.check_ingredient(query)

if __name__ == "__main__":
    main()