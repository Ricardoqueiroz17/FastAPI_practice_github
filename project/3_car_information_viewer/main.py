from fastapi import FastAPI, Query, Path, HTTPException, status, Body, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from database import cars

templates = Jinja2Templates(directory="templates")


class Car(BaseModel):
    make: Optional[str]
    model: Optional[str]
    year: Optional[int] = Field(..., ge=1970, lt=2022)
    price: Optional[float]
    engine: Optional[str] = "V4"    
    autonomous: Optional[bool]
    sold: Optional[List[str]]


app =  FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

#Testing the app.get: retrieves something in the browser, in your local host

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse

#Creating the car path: retrieve the dictionary of cars with the database of cars and their info
@app.get("/cars", response_model=List[Dict[str,Car]])

def get_cars(number: Optional[str] = Query("10", max_lenght=3)): #max_lenght - we dont want the query to pass 999 qtd
    response = []
    for id, car in list(cars.items())[:int(number)]:
        to_add = {}
        to_add[id] = car
        response.append(to_add)
    return response 

#Getting car by id
@app.get("/cars/{id}", response_model=Car)
def get_car_by_id(id: int = Path(..., ge=0, lt=1000)):
    car = cars.get(id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find car ID")
    return car

#Adding a new car: POST method
@app.post("/cars", status_code=status.HTTP_201_CREATED)
def add_cars(body_cars: List[Car], min_id: Optional[int] = Body(0)):
    if len(body_cars)<1:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="No cars to add.")
    min_id = len(cars.values()) + min_id
    for car in body_cars:
        while cars.get(min_id):
            min_id += 1
        cars[min_id] = car