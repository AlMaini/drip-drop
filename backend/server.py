from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import image_generation, virtual_tryon, clothing_analysis, health

# Initialize FastAPI app
app = FastAPI(title="Drip Drop Image Generator", description="Generate images using Gemini AI with context images")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health.router)
app.include_router(image_generation.router)
app.include_router(virtual_tryon.router)
app.include_router(clothing_analysis.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)