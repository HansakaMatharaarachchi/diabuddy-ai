from dotenv import load_dotenv

load_dotenv()

from app.routers import chat, user
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Include routers
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
