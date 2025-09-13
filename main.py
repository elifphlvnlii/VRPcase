from fastapi import FastAPI
from models import VRPInput, VRPOutput
from solver import solve_vrp_brute_force

app = FastAPI(title="VRP Solver", description="Vehicle Routing Problem Solver")

@app.get("/")
def root():
    return {"message": "VRP Solver API is running!"}

@app.post("/optimize", response_model=VRPOutput)
def solve_vrp(data: VRPInput):
    """VRP optimize endpoint"""
    return solve_vrp_brute_force(data)