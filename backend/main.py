from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import router as core_router

app = FastAPI(
    title="AGV Scheduling Exercise API",
    version="0.1.0",
    description=(
        "Modular backend for robot scheduling and simulation.\n\n"
        "Endpoints: /orders, /robots, /simulation.\n"
        "State is fully database-backed."
    ),
)

# CORS for local dev frontends (Vite/Next/CRA)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(core_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
