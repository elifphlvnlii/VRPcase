from typing import List, Tuple, Optional, Union
import itertools
from models import Vehicle, Job, VRPInput, VRPOutput, Route

# Helper fonksiyonları
def get_capacity_value(capacity: Optional[Union[int, List[int]]]) -> float:
    if capacity is None:
        return float('inf')  # Sonsuz kapasite
    if isinstance(capacity, list):
        return capacity[0] if capacity else float('inf')
    return capacity

def get_delivery_value(delivery: Optional[Union[int, List[int]]]) -> int:
    if delivery is None:
        return 1  # Default delivery miktarı
    if isinstance(delivery, list):
        return delivery[0] if delivery else 1
    return delivery

def is_valid_assignment(vehicle: Vehicle, jobs: List[Job]) -> bool:
    vehicle_capacity = get_capacity_value(vehicle.capacity)
    
    if vehicle_capacity == float('inf'):
        return True  # Sonsuz kapasite
    
    total_delivery = sum(get_delivery_value(job.delivery) for job in jobs)
    return total_delivery <= vehicle_capacity

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
    valid_assignments = 0
    
    for assignment in generate_all_assignments(jobs, vehicles):
        assignment_count += 1
        
        # Bu atama için optimal rotaları hesapla
        total_duration, routes = calculate_routes_for_assignment(data, assignment)
        
        if total_duration != float('inf'):  # Geçerli atama
            valid_assignments += 1
            if total_duration < best_total_duration:
                best_total_duration = total_duration
                best_solution = routes
    
    print(f"Toplam {assignment_count} kombinasyon denendi, {valid_assignments} geçerli")
    print(f"En iyi çözüm: {best_total_duration} saniye")
    
    if best_solution is None:
        # Hiç geçerli atama bulunamadı
        return VRPOutput(
            total_delivery_duration=0,
            routes={v.id: Route(jobs=[], delivery_duration=0) for v in vehicles}
        )
    
    return VRPOutput(
        total_delivery_duration=int(best_total_duration) if best_total_duration != float('inf') else 0,
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
        
        # Capacity kontrolü
        if not is_valid_assignment(vehicle, jobs_for_vehicle):
            return float('inf'), {}  # Geçersiz atama
        
        if not jobs_for_vehicle:
            # Boş rota
            routes[vehicle.id] = Route(jobs=[], delivery_duration=0)
            continue
        
        # Bu vehicle için en iyi job sırasını bul (service time ile)
        best_order, best_duration = find_best_job_order_with_service(
            vehicle.start_index, jobs_for_vehicle, data.matrix
        )
        
        routes[vehicle.id] = Route(
            jobs=[job.id for job in best_order],
            delivery_duration=best_duration
        )
        
        total_duration += best_duration
    
    return total_duration, routes

# Verilen başlangıç noktasından başlayarak job'ların en iyi sırasını bul (service time ile)
def find_best_job_order_with_service(start_location: int, jobs: List[Job], matrix: List[List[int]]) -> Tuple[List[Job], int]:    
    if not jobs:
        return [], 0
    
    if len(jobs) == 1:
        travel_time = matrix[start_location][jobs[0].location_index]
        service_time = jobs[0].service or 0
        return jobs, travel_time + service_time
    
    best_order = None
    best_duration = float('inf')
    
    # Tüm job sıralamarını dene
    for job_order in itertools.permutations(jobs):
        duration = calculate_route_duration_with_service(start_location, job_order, matrix)
        
        if duration < best_duration:
            best_duration = duration
            best_order = list(job_order)
    
    return best_order, best_duration

"""
# Verilen başlangıç noktasından başlayarak job'ların en iyi sırasını bul (sadece travel time)
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
"""

# Verilen bir job sırası için toplam rota süresini hesapla (travel time + service time)
def calculate_route_duration_with_service(start_location: int, jobs: List[Job], matrix: List[List[int]]) -> int:  
    if not jobs:
        return 0
    
    # Travel time hesapla
    travel_time = calculate_route_duration(start_location, jobs, matrix)
    
    # Service time ekle
    service_time = sum(job.service or 0 for job in jobs)
    
    return travel_time + service_time

# Verilen bir job sırası için toplam rota süresini hesapla (sadece travel time)
def calculate_route_duration(start_location: int, jobs: List[Job], matrix: List[List[int]]) -> int:  
    if not jobs:
        return 0
    
    current_location = start_location
    total_duration = 0
    
    for job in jobs:
        total_duration += matrix[current_location][job.location_index]
        current_location = job.location_index
    
    return total_duration

# Greedy algoritma ile VRP çözümü (capacity aware)
def solve_vrp_greedy(data: VRPInput) -> VRPOutput:
    routes = {}
    total_duration = 0
    unassigned_jobs = data.jobs.copy()
    
    print(f"Capacity-aware greedy algoritma başladı: {len(data.jobs)} job, {len(data.vehicles)} vehicle")
    
    for vehicle in data.vehicles:
        current_location = vehicle.start_index
        route_jobs = []
        route_duration = 0
        remaining_capacity = get_capacity_value(vehicle.capacity)
        
        # Bu araç için kapasiteye sığan en yakın job'ları topla
        while unassigned_jobs and remaining_capacity > 0:
            closest_job = None
            min_distance = float('inf')
            
            # Kapasiteye sığan job'lar arasından en yakınını bul
            for job in unassigned_jobs:
                delivery_amount = get_delivery_value(job.delivery)
                
                # Kapasiteye sığar mı kontrol et
                if delivery_amount <= remaining_capacity:
                    distance = data.matrix[current_location][job.location_index]
                    if distance < min_distance:
                        min_distance = distance
                        closest_job = job
            
            if closest_job:
                # Job'u rotaya ekle
                route_jobs.append(closest_job.id)
                travel_time = min_distance
                service_time = closest_job.service or 0
                route_duration += travel_time + service_time
                
                # Güncelleme yap
                current_location = closest_job.location_index
                remaining_capacity -= get_delivery_value(closest_job.delivery)
                unassigned_jobs.remove(closest_job)
            else:
                # Kapasiteye sığan job yok
                break
        
        routes[vehicle.id] = Route(
            jobs=route_jobs,
            delivery_duration=route_duration
        )
        
        total_duration += route_duration
    
    print(f"Greedy sonuç: {total_duration} saniye")
    
    return VRPOutput(
        total_delivery_duration=total_duration,
        routes=routes
    )