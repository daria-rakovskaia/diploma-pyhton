from fastapi import FastAPI
from app.api.routers import ocr_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Handwriting Recognition API",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ocr_router.router)
