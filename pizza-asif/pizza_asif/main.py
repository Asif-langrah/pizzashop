from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, create_engine
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_KEY = os.getenv("DATABASE_KEY")


# Define a Pizza model
class Pizza(SQLModel, table=True):
       id: int
       name: str
       ingredients: List[str]
       price: float
       
    


engine = create_engine(DATABASE_KEY, echo=True) 
SQLModel.metadata.create_all(engine)



   # In-memory database (for demonstration purposes)
pizzas = []


app = FastAPI()


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