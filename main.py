from fastapi import FastAPI
from models import VRPInput, VRPOutput
from solver import solve_vrp_brute_force, solve_vrp_greedy

app = FastAPI(title="VRP Solver", description="Vehicle Routing Problem Solver")

@app.get("/")
def root():
    return {"message": "VRP Solver API is running!"}

@app.post("/optimize", response_model=VRPOutput)
def solve_vrp(data: VRPInput):
    num_jobs = len(data.jobs)
    
    if num_jobs <= 6:  # Brute force threshold
        print(f"Brute force kullanılıyor")
        return solve_vrp_brute_force(data)
    else:
        print(f"Greedy kullanılıyor")
        return solve_vrp_greedy(data)

@app.post("/optimize-brute-force", response_model=VRPOutput)
def solve_vrp_force(data: VRPInput):
    return solve_vrp_brute_force(data)

@app.post("/optimize-greedy", response_model=VRPOutput)
def solve_vrp_greedy_endpoint(data: VRPInput):
    return solve_vrp_greedy(data)