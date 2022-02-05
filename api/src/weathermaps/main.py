from fastapi import FastAPI

from weathermaps.routers import weather

app = FastAPI()


app.include_router(weather.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
