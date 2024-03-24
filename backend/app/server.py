from app.dependencies.auth import VerifyToken
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Security
from fastapi.responses import RedirectResponse
from langserve import add_routes

load_dotenv()

auth = VerifyToken()

app = FastAPI(
    dependencies=[Depends(Security(auth.verify))],
)


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# Edit this to add the chain you want to add
add_routes(app, chat_chain, path="/chat")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
