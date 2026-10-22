FROM python:3.11-slim

WORKDIR /app

# Build tools are not required for the pinned binary wheels used by this app.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
