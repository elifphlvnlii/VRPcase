from typing import List, Tuple
import itertools
from models import Vehicle, Job, VRPInput, VRPOutput, Route

# Brute force VRP solver, tüm kombinasyonları dene
def solve_vrp_brute_force(data: VRPInput) -> VRPOutput:
    jobs = data.jobs
    vehicles = data.vehicles
    
    if not jobs:
        # Job yoksa boş rotalar döndür
        return VRPOutput(
            total_delivery_duration=0,
            routes={v.id: Route(jobs=[], delivery_duration=0) for v in vehicles}
        )
    
    best_solution = None
    best_total_duration = float('inf')
    
    print(f"Brute force başladı: {len(jobs)} job, {len(vehicles)} vehicle")
    
    # Tüm job'ları vehicle'lara atama kombinasyonları
    assignment_count = 0
    for assignment in generate_all_assignments(jobs, vehicles):
        assignment_count += 1
        
        # Bu atama için optimal rotaları hesapla
        total_duration, routes = calculate_routes_for_assignment(data, assignment)
        
        if total_duration < best_total_duration:
            best_total_duration = total_duration
            best_solution = routes
    
    print(f"Toplam {assignment_count} kombinasyon denendi")
    print(f"En iyi çözüm: {best_total_duration} saniye")
    
    return VRPOutput(
        total_delivery_duration=best_total_duration,
        routes=best_solution
    )


# Tüm job'ları vehicle'lara atama kombinasyonlarını üret
def generate_all_assignments(jobs: List[Job], vehicles: List[Vehicle]):
    num_jobs = len(jobs)
    num_vehicles = len(vehicles)
    
    # Her job için hangi vehicle'a gideceğini belirle (0, num_vehicles-1)
    for assignment in itertools.product(range(num_vehicles), repeat=num_jobs):
        yield assignment


# Verilen bir atama için her vehicle'ın rotasını ve toplam süreyi hesapla
def calculate_routes_for_assignment(data: VRPInput, assignment: Tuple[int]) -> Tuple[int, dict]:
    routes = {}
    total_duration = 0
    
    # Her vehicle için job listesi oluştur
    vehicle_jobs = {i: [] for i in range(len(data.vehicles))}
    
    for job_idx, vehicle_idx in enumerate(assignment):
        vehicle_jobs[vehicle_idx].append(data.jobs[job_idx])
    
    # Her vehicle için optimal rota sırası bul
    for vehicle_idx, vehicle in enumerate(data.vehicles):
        jobs_for_vehicle = vehicle_jobs[vehicle_idx]
        
        if not jobs_for_vehicle:
            # Boş rota
            routes[vehicle.id] = Route(jobs=[], delivery_duration=0)
            continue
        
        # Bu vehicle için en iyi job sırasını bul
        best_order, best_duration = find_best_job_order(
            vehicle.start_index, jobs_for_vehicle, data.matrix
        )
        
        routes[vehicle.id] = Route(
            jobs=[job.id for job in best_order],
            delivery_duration=best_duration
        )
        
        total_duration += best_duration
    
    return total_duration, routes


# Verilen başlangıç noktasından başlayarak job'ların en iyi sırasını bul
def find_best_job_order(start_location: int, jobs: List[Job], matrix: List[List[int]]) -> Tuple[List[Job], int]:    
    if not jobs:
        return [], 0
    
    if len(jobs) == 1:
        duration = matrix[start_location][jobs[0].location_index]
        return jobs, duration
    
    best_order = None
    best_duration = float('inf')
    
    # Tüm job sıralamarını dene
    for job_order in itertools.permutations(jobs):
        duration = calculate_route_duration(start_location, job_order, matrix)
        
        if duration < best_duration:
            best_duration = duration
            best_order = list(job_order)
    
    return best_order, best_duration


# Verilen bir job sırası için toplam rota süresini hesapla
def calculate_route_duration(start_location: int, jobs: List[Job], matrix: List[List[int]]) -> int:  
    if not jobs:
        return 0
    
    current_location = start_location
    total_duration = 0
    
    for job in jobs:
        total_duration += matrix[current_location][job.location_index]
        current_location = job.location_index
    
    return total_duration