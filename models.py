from pydantic import BaseModel
from typing import List, Optional, Union

class Vehicle(BaseModel):
    id: int 
    start_index: int
    capacity: Optional[Union[int, List[int]]] = None

class Job(BaseModel):
    id: int
    location_index: int
    delivery: Optional[Union[int, List[int]]] = None  
    service: Optional[int] = None

class VRPInput(BaseModel):
    vehicles: List[Vehicle]
    jobs: List[Job]
    matrix: List[List[int]]

class Route(BaseModel):
    jobs: List[int]  
    delivery_duration: int

class VRPOutput(BaseModel):
    total_delivery_duration: int
    routes: dict[int, Route]