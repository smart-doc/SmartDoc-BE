from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.__init__ import api_router

app = FastAPI(
    title="Medical App API",
    description="API for medical consultation application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "SmartDoc API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}