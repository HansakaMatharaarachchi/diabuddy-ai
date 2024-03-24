from dotenv import load_dotenv

load_dotenv()

from app.routers import user
from fastapi import FastAPI, Security
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Include routers
app.include_router(user.router, prefix="/user", tags=["user"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
