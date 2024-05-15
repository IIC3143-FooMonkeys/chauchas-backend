from config.database import discountsTable

def insert_tests():
    discountsTable.insert_one(
        {
            "name": "papa yon piza",
            "category": "Food"
        }
    )

    discountsTable.insert_one(
        {
            "name": "burga de las K",
            "category": "Food"
        }
    )