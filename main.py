from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI(title="VRP Solver", description="Vehicle Routing Problem Solver")

# Input data models
class Vehicle(BaseModel):
    id: str
    start_index: int
    capacity: Optional[int] = None

class Job(BaseModel):
    id: str
    location_index: int
    delivery: Optional[int] = None
    service: Optional[int] = None

class VRPInput(BaseModel):
    vehicles: List[Vehicle]
    jobs: List[Job]
    matrix: List[List[int]]

# Output data models
class Route(BaseModel):
    jobs: List[str]
    delivery_duration: int

class VRPOutput(BaseModel):
    total_delivery_duration: int
    routes: dict[str, Route]

@app.post("/optimize", response_model=VRPOutput)
def solve_vrp(data: VRPInput):
    # Test implementation: returns empty routes and zero duration   
    return {
        "total_delivery_duration": 0,
        "routes": {
            vehicle.id: {
                "jobs": [],
                "delivery_duration": 0
            } for vehicle in data.vehicles
        }
    }

@app.get("/")
def root():
    return {"message": "VRP Solver API is running!"}