from routes.route import router
from routes.categories import router as categories_router
from routes.discounts import router as discounts_router
from routes.banks import router as banks_router
import uvicorn
from fastapi import FastAPI
from test_database.insertions import insert_tests

app = FastAPI()
app.include_router(router)
app.include_router(categories_router)
app.include_router(discounts_router)
app.include_router(banks_router)

if __name__ == '__main__':
    #insert_tests()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)