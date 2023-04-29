
from fastapi import FastAPI
import uvicorn
from Routers import taxi
import sklearn

print(f"sklearn version: {sklearn.__version__}")
print(f"uvicorn version: {uvicorn.__version__}")

app = FastAPI(title="REST API")
app.include_router(taxi.router)


@app.get("/")
async def welcome() -> dict:
    return {"result": "Welcome to New York City Taxi REST API"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
