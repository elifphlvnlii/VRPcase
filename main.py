from fastapi import FastAPI, HTTPException
from models import VRPInput, VRPOutput
from bruteforce_solver import solve_vrp_brute_force
from greedy_solver import solve_vrp_greedy
import json
import os

app = FastAPI(title="VRP Solver", description="Vehicle Routing Problem Solver")

# Input dosyası kullanarak VRP çözen endpoint
@app.post("/optimize-file", response_model=VRPOutput)
def solve_vrp_from_file(filename: str = "input.json"):
    try:
        if not os.path.exists(filename):
            raise HTTPException(status_code=404, detail=f"Dosya bulunamadı: {filename}")
        
        # JSON dosyasını oku
        with open(filename, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
        
        # JSON'u VRPInput modeline çevir
        data = VRPInput(**data_dict)
        
        # Çözüm fonksiyonu çağır
        num_jobs = len(data.jobs)
        
        if num_jobs <= 10: # threshold
            print(f"Dosyadan küçük problem ({num_jobs} jobs) - Brute force kullanılıyor")
            return solve_vrp_brute_force(data)
        else:
            print(f"Dosyadan büyük problem ({num_jobs} jobs) - Greedy kullanılıyor")
            return solve_vrp_greedy(data)
            
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Geçersiz JSON formatı: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya işleme hatası: {str(e)}")

@app.get("/optimize", response_model=VRPOutput)
def solve_vrp():
    return solve_vrp_from_file("input.json")