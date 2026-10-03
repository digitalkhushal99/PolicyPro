import json
import faiss
from sentence_transformers import SentenceTransformer

index = faiss.read_index("index/policies.faiss")
chunks = json.load(open("index/chunks.json", encoding="utf-8"))
model = SentenceTransformer("all-MiniLM-L6-v2")

questions = [
    "Can I accept a gift from a vendor?",
    "How do I report sexual harassment at work?",
    "What personal data does Infosys collect?",
    "What should I do if a government official asks for a bribe?",
]

for q in questions:
    vec = model.encode([q], normalize_embeddings=True).astype("float32")
    scores, ids = index.search(vec, 3)
    print(f"\nQ: {q}")
    for score, i in zip(scores[0], ids[0]):
        c = chunks[i]
        print(f"  [{score:.2f}] {c['source']} p.{c['page']}: {c['text'][:110]}...")