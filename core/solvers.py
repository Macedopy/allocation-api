import heapq
import time
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from .domain import Cargo, Vehicle, AllocationResult
from .interfaces import ISolver

@dataclass(order=True)
class Node:
    neg_bound: float
    level: int = field(compare=False)
    val: float = field(compare=False)
    res_peso: Tuple[float, ...] = field(compare=False)
    res_comp: Tuple[float, ...] = field(compare=False)
    assign: Tuple[int, ...] = field(compare=False)

class BranchAndBoundSolver(ISolver):
    def __init__(self):
        self.nodes_explored = 0

    def solve(self, cargos: List[Cargo], vehicles: List[Vehicle]) -> AllocationResult:
        start_time = time.time()
        self.nodes_explored = 0
        
        # Sort cargos by value density for B&B efficiency
        sorted_cargos = sorted(cargos, key=lambda x: x.value_per_weight, reverse=True)
        n = len(sorted_cargos)
        k = len(vehicles)

        # Initial greedy solution (Lower Bound)
        best_val, best_asg = self._greedy(sorted_cargos, vehicles)
        
        init_rp = tuple(v.cap_peso for v in vehicles)
        init_rc = tuple(v.comp for v in vehicles)
        root_b = self._upper_bound(0, 0, list(init_rp), list(init_rc), sorted_cargos, vehicles)
        
        root = Node(-root_b, 0, 0.0, init_rp, init_rc, tuple([-1] * n))
        heap = [root]

        while heap:
            node = heapq.heappop(heap)
            self.nodes_explored += 1

            if -node.neg_bound <= best_val:
                continue
            
            if node.level == n:
                if node.val > best_val:
                    best_val, best_asg = node.val, list(node.assign)
                continue

            it = sorted_cargos[node.level]
            
            # BRANCH 1: Include in the best viable vehicle
            viable = [i for i in range(k) if self._fits(it, vehicles[i], node.res_peso[i], node.res_comp[i])]
            if viable:
                # Heuristic: pick vehicle with most residual length
                best_k = max(viable, key=lambda i: node.res_comp[i])
                
                new_rp = list(node.res_peso)
                new_rc = list(node.res_comp)
                new_rp[best_k] -= it.peso
                new_rc[best_k] -= it.comp
                
                new_asg = list(node.assign)
                new_asg[node.level] = vehicles[best_k].id # Store actual vehicle ID
                new_val = node.val + it.val
                
                b = self._upper_bound(new_val, node.level + 1, new_rp, new_rc, sorted_cargos, vehicles)
                if b > best_val:
                    heapq.heappush(heap, Node(-b, node.level + 1, new_val, tuple(new_rp), tuple(new_rc), tuple(new_asg)))
                    if new_val > best_val:
                        best_val, best_asg = new_val, new_asg

            # BRANCH 2: Exclude
            b = self._upper_bound(node.val, node.level + 1, list(node.res_peso), list(node.res_comp), sorted_cargos, vehicles)
            if b > best_val:
                heapq.heappush(heap, Node(-b, node.level + 1, node.val, node.res_peso, node.res_comp, node.assign))

        # Re-map assignments to original cargo IDs
        # Since we sorted cargos, we need to be careful. 
        # Actually, let's return a list where index corresponds to the input cargos list.
        final_assignments = [-1] * len(cargos)
        for i, vehicle_id in enumerate(best_asg):
            cargo_original_id = sorted_cargos[i].id
            # Find index of this cargo in original list
            for idx, orig_c in enumerate(cargos):
                if orig_c.id == cargo_original_id:
                    final_assignments[idx] = vehicle_id
                    break

        return AllocationResult(
            total_value=best_val,
            allocations=final_assignments,
            execution_time=time.time() - start_time,
            nodes_explored=self.nodes_explored
        )

    def _fits(self, cargo: Cargo, vehicle: Vehicle, res_peso: float, res_comp: float) -> bool:
        return (cargo.peso <= res_peso and
                cargo.alt <= vehicle.alt and
                cargo.larg <= vehicle.larg and
                cargo.comp <= res_comp)

    def _upper_bound(self, val: float, level: int, res_peso: List[float], res_comp: List[float], cargos: List[Cargo], vehicles: List[Vehicle]) -> float:
        bound = val
        n = len(cargos)
        k = len(vehicles)
        rp = res_peso[:]
        rc = res_comp[:]
        
        for i in range(level, n):
            it = cargos[i]
            candidates = [j for j in range(k) if it.alt <= vehicles[j].alt and it.larg <= vehicles[j].larg]
            if not candidates: continue
            
            best_j = max(candidates, key=lambda j: rc[j])
            if rp[best_j] <= 0 or rc[best_j] <= 0: continue
            
            frac = min(
                min(rp[best_j], it.peso) / it.peso,
                min(rc[best_j], it.comp) / it.comp
            )
            bound += it.val * frac
            rp[best_j] -= it.peso * frac
            rc[best_j] -= it.comp * frac
        return bound

    def _greedy(self, cargos: List[Cargo], vehicles: List[Vehicle]) -> Tuple[float, List[int]]:
        rp = [v.cap_peso for v in vehicles]
        rc = [v.comp for v in vehicles]
        asg = [-1] * len(cargos)
        val = 0.0
        for i, it in enumerate(cargos):
            # Sort vehicles by residual length descending
            for k in sorted(range(len(vehicles)), key=lambda idx: -rc[idx]):
                if self._fits(it, vehicles[k], rp[k], rc[k]):
                    asg[i] = vehicles[k].id
                    rp[k] -= it.peso
                    rc[k] -= it.comp
                    val += it.val
                    break
        return val, asg
    