from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class Cargo:
    id: int
    name: str
    peso: float
    alt: float
    larg: float
    comp: float
    val: float

    @property
    def value_per_weight(self) -> float:
        return self.val / self.peso if self.peso > 0 else 0

@dataclass(frozen=True)
class Vehicle:
    id: int
    nome: str
    cap_peso: float
    alt: float
    larg: float
    comp: float

@dataclass
class AllocationResult:
    total_value: float
    allocations: List[Optional[int]]  # Index is Cargo, Value is Vehicle ID or -1
    execution_time: float
    nodes_explored: int
