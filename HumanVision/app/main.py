from __future__ import annotations

from api.api import api_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Human Vision Prediction', version='1.0.0')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include the new router with a clean prefix
app.include_router(api_router, prefix='/api')

if __name__ == "__main__":
    import uvicorn

    # Start the server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
