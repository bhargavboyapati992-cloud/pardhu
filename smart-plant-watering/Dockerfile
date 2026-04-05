# --- Stage 1: Build Frontend Dashboard ---
FROM node:20-alpine as frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build


# --- Stage 2: Set up Python Backend & Serve API + Frontend ---
FROM python:3.11-slim
WORKDIR /app/backend

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./

# Copy the built React app from Stage 1 so FastAPI can serve it
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose Cloud Run's required port
EXPOSE 8080

# Run the FastAPI server natively
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
