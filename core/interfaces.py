from abc import ABC, abstractmethod
from typing import List
from .domain import Cargo, Vehicle, AllocationResult

class ISolver(ABC):
    @abstractmethod
    def solve(self, cargos: List[Cargo], vehicles: List[Vehicle]) -> AllocationResult:
        """Solves the allocation problem."""
        pass
