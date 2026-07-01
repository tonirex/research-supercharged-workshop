# Research Tools MCP server — container image for Azure Container Apps.
# Built in the cloud by `az containerapp up --source .` (no local Docker needed).
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py ./

EXPOSE 8000

# Streamable HTTP transport -> MCP endpoint served at http://0.0.0.0:8000/mcp
CMD ["python", "server.py"]
