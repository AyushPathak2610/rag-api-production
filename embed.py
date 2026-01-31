import chromadb 

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="docs")

with open("k8s.txt", "r") as f:
    data = f.read()

collection.add(documents=[data], ids=["k8s"])

print("Data added to the collection.")