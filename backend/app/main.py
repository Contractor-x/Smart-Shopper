from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search, scrape, analyze

app = FastAPI(title="SmartShopper AI")

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(search.router, prefix="/api")
app.include_router(scrape.router, prefix="/api")
app.include_router(analyze.router, prefix="/api")
