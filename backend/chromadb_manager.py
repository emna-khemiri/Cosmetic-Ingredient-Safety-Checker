import chromadb
from chromadb.utils import embedding_functions

class ChromaDBManager:
    """Manage ChromaDB operations for COSING data."""
    def __init__(self, collection_name):
        self.client = chromadb.Client()
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(collection_name)

    def populate(self, json_files):
        """Populate ChromaDB with COSING data."""
        if self.collection.count() > 0:
            print("ChromaDB already populated.")
            return

        documents = []
        metadatas = []
        ids = []
        seen_ids = set()

        for category, data in json_files.items():
            for idx, item in enumerate(data):
                names = item.get("Name of Common Ingredients Glossary", "").split(" / ")
                if not names or not names[0].strip():
                    names = item.get("Identified INGREDIENTS or substances e.g.", "").split("\n")
                chemical_name = item.get("Chemical name / INN / XAN", "") or item.get("Chemical/IUPAC Name", "")
                restrictions = (
                    item.get("Restrictions: Maximum concentration in ready for use preparation", "") or
                    item.get("Conditions: Maximum concentration in ready for use preparation", "") or
                    ""
                )
                conditions = item.get("Restrictions: Other", "") or item.get("Conditions: Other", "") or ""
                regulation = item.get("Regulation", "")
                sccs_opinions = item.get("SCCS opinions", "")
                product_type = item.get("Conditions: Product Type, body parts", "") or ""
                warnings = item.get("Wording of conditions of use and warnings", "") or ""

                for name_idx, name in enumerate(names):
                    if not name.strip():
                        continue
                    base_id = f"{category}_{idx}_{name.lower().replace(' ', '_').replace('(', '').replace(')', '')}"
                    unique_id = f"{base_id}_{name_idx}"
                    
                    if unique_id in seen_ids:
                        print(f"Warning: Duplicate ID detected: {unique_id} for {name} in {category}. Skipping.")
                        continue
                    seen_ids.add(unique_id)

                    text = f"{name} {chemical_name} {restrictions} {conditions} {regulation} {sccs_opinions} {product_type} {warnings}".strip()
                    documents.append(text)
                    metadatas.append({
                        "category": category,
                        "name": name.lower(),
                        "chemical_name": chemical_name,
                        "restrictions": restrictions,
                        "conditions": conditions,
                        "regulation": regulation,
                        "sccs_opinions": sccs_opinions,
                        "product_type": product_type,
                        "warnings": warnings
                    })
                    ids.append(unique_id)

        if documents:
            try:
                self.collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=self.embedding_function(documents)
                )
                print(f"Populated ChromaDB with {len(documents)} entries.")
            except chromadb.errors.DuplicateIDError as e:
                print(f"Error: Duplicate IDs detected during ChromaDB population: {e}")

    def query(self, query_text, top_k=3):
        """Query ChromaDB for ingredient information."""
        results = self.collection.query(
            query_texts=[query_text.lower().strip()],
            n_results=top_k
        )
        retrieved = []
        for i in range(len(results["ids"][0])):
            metadata = results["metadatas"][0][i]
            category = metadata["category"]
            details = (
                "Banned under EU regulations" if category == "prohibited" else
                f"Restricted: {metadata['restrictions']} {metadata['conditions']}".strip() if category == "restricted" else
                f"Allowed as {'colorant' if category == 'colorants' else 'preservative' if category == 'preservatives' else 'UV filter'}: {metadata['restrictions']}".strip()
            )
            if metadata["product_type"]:
                details += f" (Product Type: {metadata['product_type']})"
            if metadata["warnings"]:
                details += f" (Warnings: {metadata['warnings']})"
            retrieved.append({
                "name": metadata["name"],
                "category": category,
                "details": details,
                "regulation": metadata["regulation"],
                "sccs_opinions": metadata["sccs_opinions"]
            })
        return retrieved if retrieved else [{"name": query_text, "category": "unknown", "details": "Not found in COSING database"}]