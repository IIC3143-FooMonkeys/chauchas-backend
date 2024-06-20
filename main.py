from routes.route import router
from routes.categories import router as categories_router
import uvicorn
from fastapi import FastAPI
from test_database.insertions import insert_tests

app = FastAPI()
app.include_router(router)
app.include_router(categories_router)

if __name__ == '__main__':
    #insert_tests()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)