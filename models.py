from pydantic import BaseModel
from typing import List, Optional

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

class Route(BaseModel):
    jobs: List[str]
    delivery_duration: int

class VRPOutput(BaseModel):
    total_delivery_duration: int
    routes: dict[str, Route]