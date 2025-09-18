from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import goals, suggestions, stats
from mock_data import initialize_mock_data

app = FastAPI(
    title="Proactive Goal Coach API",
    description="API para assistente pessoal de objetivos",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(goals.router, prefix="/api/goals", tags=["goals"])
app.include_router(suggestions.router, prefix="/api/suggestions", tags=["suggestions"])
app.include_router(stats.router, prefix="/api/stats", tags=["stats"])

@app.on_event("startup")
async def startup_event():
    initialize_mock_data()

@app.get("/")
async def root():
    return {"message": "Proactive Goal Coach API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}