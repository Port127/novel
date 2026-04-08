from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import (
    projects,
    characters,
    worldbuilding,
    chapters,
    plot,
    timeline,
    relationships,
    compliance,
    quality,
    llm,
    skills,
)

app = FastAPI(
    title="Novel Writing System API",
    version="0.1.0",
    description="Backend API for the AI novel writing workbench",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)
app.include_router(characters.router)
app.include_router(worldbuilding.router)
app.include_router(chapters.router)
app.include_router(plot.router)
app.include_router(timeline.router)
app.include_router(relationships.router)
app.include_router(compliance.router)
app.include_router(quality.router)
app.include_router(llm.router)
app.include_router(skills.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["backend"])
