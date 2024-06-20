from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.main import router
from routes.categories import router as categories_router
from routes.discounts import router as discounts_router
from routes.banks import router as banks_router
from routes.cards import router as cards_router
from routes.users import router as users_router
import uvicorn

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(categories_router)
app.include_router(discounts_router)
app.include_router(banks_router)
app.include_router(cards_router)
app.include_router(users_router)

if __name__ == '__main__':
    #insert_tests()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
