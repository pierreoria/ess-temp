from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# Classe - produto
class Product(BaseModel):
    name : str
    category: str
    price : int
    quantity : int

# File to store product data
PRODUCT_DATA_FILE = "product_data.json"

# Helper function to load user data from JSON file
def load_product_data():
    try:
        with open(PRODUCT_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Helper function to save user data to JSON file
def save_product_data(data):
    with open(PRODUCT_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# segunda etapa vai ser mapear loja pra produto. só mostrar produtos daquela loja

# Endpoint for adding new product
@app.post("/products/add_new_product")
async def add_product(name: str, price: int, quantity : int, category : str = "outros"):

    product = Product(name = name, price = price, quantity = quantity, category = category)
    product_data = load_product_data()
    
    # erro: produto já existente
    if product.name in product_data:
        raise HTTPException(status_code=400, detail="Product already exists")
    
    # modifica json
    product_data[product.name] = {
    "price" : product.price,
    "category" : product.category,
    "quantity": product.quantity
    }

    # salva json
    save_product_data(product_data)
    
    return {"message": "Product added successfully"}



@app.get("/products/{product_name}")
async def modify_product(product_name: str, price: int, quantity: int, category: str):
    product_data = load_product_data()
    
    # Check if product exists
    if product_name not in product_data:
        raise HTTPException(status_code=404, detail="Product not found")

    # modifica json
    product_data[product_name] = {
    "price" : price,
    "category" : category,
    "quantity": quantity
    }

    # Save updated product data
    save_product_data(product_data)

    return {"message": "Product modified successfully"}


