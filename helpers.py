from typing import List, Optional, Union
from models import Vehicle, Job

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