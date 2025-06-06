# provaia/backend/src/provaia/main.py

"""
===============================================================================
PROVAIA MAIN MODULE
===============================================================================
This module initializes the FastAPI server for the ProvaIA system, responsible
for automatically generating personalized exams using Google Classroom and the
OpenAI API.

===============================================================================
FEATURES
===============================================================================
1. **FastAPI Initialization**:
   - Creates and configures a FastAPI instance for serving HTTP requests.

2. **CORS Middleware Setup**:
   - Configures Cross-Origin Resource Sharing (CORS) to manage frontend-backend interactions.

3. **API Routing**:
   - Includes API routes defined in the `routes.py` module.

4. **Health Check Endpoint**:
   - Provides a simple endpoint to verify if the API is running.

===============================================================================
HOW TO USE
===============================================================================
1. **Start the API Server**:
   - Run the following command from the backend directory:
     ```bash
     poetry run uvicorn src.provaia.main:app --reload
     ```

2. **Verify Server Status**:
   - Access `http://localhost:8000/` in a web browser or via curl:
     ```bash
     curl http://localhost:8000/
     ```
     Response:
     ```json
     {"message": "ProvaIA API is running!"}
     ```

===============================================================================
DEPENDENCIES
===============================================================================
- FastAPI
- CORSMiddleware (FastAPI built-in middleware)
- Uvicorn (server)

===============================================================================
AUTHOR
===============================================================================
- Paulo César Rodacki Gomes
- Email: rodacki@gmail.com
- Last Updated: 2024-03-10
===============================================================================
"""

# ----------------------------------------
# IMPORTS
# ----------------------------------------
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from src.provaia.api.routes import router

# ----------------------------------------
# CONFIGURATIONS
# ----------------------------------------

# Creating FastAPI instance
app = FastAPI(
    title="ProvaIA API",
    description="API para geração automática de provas a partir do Google Classroom e OpenAI",
    version="1.0"
)

# Configuring CORS middleware (adjust allow_origins for increased security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change as needed for security
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ----------------------------------------
# ROUTES
# ----------------------------------------

# Including API routes defined in routes.py
app.include_router(router)

# ----------------------------------------
# ENDPOINTS
# ----------------------------------------

@app.get("/")
def health_check():
    """
    Health check endpoint to verify if the API server is running.

    Returns:
        dict: A message indicating the API is operational.
    """
    return {"message": "ProvaIA API is running!"}


@app.options("/{full_path:path}")
async def preflight_request(full_path: str, response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "OPTIONS, GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response