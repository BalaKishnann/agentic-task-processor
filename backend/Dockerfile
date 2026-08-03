FROM python:3.12-slim

WORKDIR /app

# Install dependencies first, separately from app code, so Docker's
# layer cache skips this step on rebuilds unless requirements.txt changed.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

EXPOSE 8000

# --host 0.0.0.0 is required inside a container — 127.0.0.1 (uvicorn's
# default) would only accept connections from inside the container itself.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]