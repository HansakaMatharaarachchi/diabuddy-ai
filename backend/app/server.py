from dotenv import load_dotenv

load_dotenv()

from app.routers import chats, users
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="DiaBuddy API",
    description="API for DiaBuddy chatbot",
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Include routers.
app.include_router(
    users.router,
    prefix="/api/users",
    tags=["users"],
)
app.include_router(chats.router, prefix="/api/users", tags=["chats"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
