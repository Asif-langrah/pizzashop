from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel 
from typing import List, Optional


DATBASE_KEY = 'postgresql://neondb_owner:LAYBh2ETrNs0@ep-shrill-shadow-a1dtu58s.ap-southeast-1.aws.neon.tech/friday-db?sslmode=require'

app = FastAPI()

   # Define a Pizza model
class Pizza(SQLModel):
       id: int
       name: str
       ingredients: List[str]
       price: float

   # In-memory database (for demonstration purposes)
pizzas = []

   # Get all pizzas
@app.get("/pizzas", response_model=List[Pizza])
def get_pizzas():
       return pizzas

   # Get a single pizza by ID
@app.get("/pizzas/{pizza_id}", response_model=Pizza)
def get_pizza(pizza_id: int):
       pizza = next((pizza for pizza in pizzas if pizza.id == pizza_id), None)
       if pizza is None:
           raise HTTPException(status_code=404, detail="Pizza not found")
       return pizza
 # Create a new pizza
@app.post("/pizzas", response_model=Pizza)
def create_pizza(pizza: Pizza):
       if any(p for p in pizzas if p.id == pizza.id):
           raise HTTPException(status_code=400, detail="Pizza with this ID already exists")
       pizzas.append(pizza)
       return pizza

   # Update an existing pizza
@app.put("/pizzas/{pizza_id}", response_model=Pizza)
def update_pizza(pizza_id: int, updated_pizza: Pizza):
       index = next((i for i, pizza in enumerate(pizzas) if pizza.id == pizza_id), None)
       if index is None:
           raise HTTPException(status_code=404, detail="Pizza not found")
       pizzas[index] = updated_pizza
       return updated_pizza

   # Delete a pizza
@app.delete("/pizzas/{pizza_id}")
def delete_pizza(pizza_id: int):
       global pizzas
       pizzas = [pizza for pizza in pizzas if pizza.id != pizza_id]
       return {"message": "Pizza deleted successfully"}