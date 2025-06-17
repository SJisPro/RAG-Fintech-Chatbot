import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="company_docs")


def add_document(doc_id, content, metadata):
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[doc_id]
    )

def search(query, n_results=3, filter_by=None):
    if filter_by:  
        return collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"category": {"$in": filter_by}}
        )
    else:  
        return collection.query(
            query_texts=[query],
            n_results=n_results
        )