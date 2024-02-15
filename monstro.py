from fastapi import FastAPI, HTTPException, Depends, Cookie, Path, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import json

app = FastAPI()

# Model for user credentials
class User(BaseModel):
    username: str
    password: str

# File to store user data
USER_DATA_FILE = "user_data.json"

# Helper function to load user data from JSON file
def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Helper function to save user data to JSON file
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Endpoint for user sign-up
@app.post("/signup/")
async def signup(u: str, p: str):
    user = User(username=u, password=p)
    user_data = load_user_data()
    if user.username in user_data:
        raise HTTPException(status_code=400, detail="Username already exists")
    user_data[user.username] = {"password": user.password}
    save_user_data(user_data)
    return {"message": "User signed up successfully"}

# Endpoint for user login
@app.post("/login/")
async def login(username: str, password: str):
    user_data = load_user_data()
    if username not in user_data or user_data[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    response = RedirectResponse(url=f"/auth/{username}", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="username", value=username)
    return response

# Dependency to check if user is logged in
def get_current_user(username: str = Cookie(None)):
    user_data = load_user_data()
    if username not in user_data:
        raise HTTPException(status_code=401, detail="You must be logged in")
    return username

# página individual
@app.get("/auth/{user}")
async def user_page(user: str = Depends(get_current_user)):
    return {"message": f"Welcome, {user}!"}

# Classe - produto
class Product(BaseModel):
    loja : str
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

# Endpoint for adding new product
@app.post("/auth/{user}/products/add_new")
async def add_product(
    name: str, 
    price: int, 
    quantity : int, 
    category : str = "outros", 
    user: str = Depends(get_current_user)
    ):

    product = Product(
        loja = user,
        name = name, 
        price = price, 
        quantity = quantity, 
        category = category
    )
    
    product_data = load_product_data()
    
    # erro: produto já existente
    if product.name in product_data:
        raise HTTPException(status_code=400, detail="Product already exists")
    
    # modifica json
    product_data[product.name] = {
        "loja" : product.loja,
        "price" : product.price,
        "category" : product.category,
        "quantity": product.quantity
    }

    # salva json
    save_product_data(product_data)
    
    return {"message": "Product added successfully"}



@app.get("/auth/{user}/products/{product_name}")
async def modify_product(
    product_name: str, 
    price: int, 
    quantity: int, 
    category: str, 
    user: str = Depends(get_current_user)
    ):
    
    product_data = load_product_data()
    
    # Check if product exists
    if product_name not in product_data:
        raise HTTPException(status_code=404, detail="Product not found")

    # modifica json: apenas campos fornecidos (mantém loja e nome)
    # versões futuras suportarão campos vazios, deixar assim
    if price is not None:
        product_data[product_name]["price"] = price
    if category is not None:
        product_data[product_name]["category"] = category
    if quantity is not None:
        product_data[product_name]["quantity"] = quantity

    # Save updated product data
    save_product_data(product_data)

    return {"message": "Product modified successfully"}
