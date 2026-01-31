# FROM python:3.11-slim

# # 1. App lives here
# WORKDIR /app

# # 2. System deps (curl is useful for debugging)
# RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# # 3. Copy source code
# COPY app.py embed.py k8s.txt ./

# # 4. Install Python deps (no requirements.txt needed)
# RUN pip install --no-cache-dir fastapi uvicorn chromadb ollama

# # 5. Expose FastAPI port (documentation only)
# EXPOSE 8000

# # 6. Start FastAPI (runtime only!)
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.11-slim

# 1. App lives here
WORKDIR /app

# 2. System deps (curl useful for debugging)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 3. Copy source code
COPY app.py embed.py k8s.txt ./

# 4. Install Python deps
RUN pip install --no-cache-dir fastapi uvicorn chromadb ollama

# 5. BUILD-TIME step: create embeddings
RUN python embed.py

# 6. Document exposed port
EXPOSE 8000

# 7. RUNTIME: start API only
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
