from models import VRPInput, VRPOutput, Route
from helpers import get_capacity_value, get_delivery_value

# Greedy algoritma ile VRP çözümü (capacity aware)
def solve_vrp_greedy(data: VRPInput) -> VRPOutput:
    routes = {}
    total_duration = 0
    unassigned_jobs = data.jobs.copy()
    
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
    
    return VRPOutput(
        total_delivery_duration=total_duration,
        routes=routes
    )