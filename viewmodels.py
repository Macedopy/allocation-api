from typing import List, Dict, Any
from .models import Truck, Load
from .core.domain import Cargo, Vehicle, AllocationResult
from .core.interfaces import ISolver
from .core.solvers import BranchAndBoundSolver

class AllocationViewModel:
    # MOCK TRUCKS as requested
    MOCK_TRUCKS = [
        {"id": 0, "nome": "Semireboque-01", "cap_peso": 28000, "alt": 2.9, "larg": 2.5, "comp": 14.5},
        {"id": 1, "nome": "Semireboque-02", "cap_peso": 25000, "alt": 2.8, "larg": 2.4, "comp": 13.5},
        {"id": 2, "nome": "Frigorifico-01", "cap_peso": 22000, "alt": 2.6, "larg": 2.3, "comp": 13.0},
        {"id": 3, "nome": "Frigorifico-02", "cap_peso": 20000, "alt": 2.55, "larg": 2.25, "comp": 12.5},
        {"id": 4, "nome": "Bitren-01", "cap_peso": 42000, "alt": 3.0, "larg": 2.6, "comp": 25.0},
        {"id": 5, "nome": "Bitren-02", "cap_peso": 38000, "alt": 2.9, "larg": 2.5, "comp": 24.0},
        {"id": 6, "nome": "Rodotrem-01", "cap_peso": 57000, "alt": 3.2, "larg": 2.6, "comp": 30.0},
        {"id": 7, "nome": "Truck-01", "cap_peso": 15000, "alt": 2.7, "larg": 2.4, "comp": 10.0},
        {"id": 8, "nome": "Truck-02", "cap_peso": 13000, "alt": 2.6, "larg": 2.3, "comp": 9.0},
        {"id": 9, "nome": "VUC-01", "cap_peso": 8000, "alt": 2.4, "larg": 2.1, "comp": 7.0}
    ]

    def __init__(self, solver: ISolver = None):
        self.solver = solver or BranchAndBoundSolver()

    def get_allocation_plan(self) -> Dict[str, Any]:
        """
        Fetches loads from DB, expands them by quantity, 
        uses mock trucks, runs the solver, and returns a formatted plan.
        """
        # 1. Use Mock Trucks
        vehicles = [Vehicle(**t) for t in self.MOCK_TRUCKS]

        # 2. Fetch Loads and expand by quantity
        load_queryset = Load.objects.all()
        cargos = []
        global_cargo_id = 1
        
        for l in load_queryset:
            # Expand quantity: create 'n' separate Cargo objects
            for _ in range(l.quantidade):
                cargos.append(
                    Cargo(
                        id=global_cargo_id,
                        name=f"{l.name} #{_ + 1}", # Unique name for each item
                        peso=l.peso,
                        alt=l.alt,
                        larg=l.larg,
                        comp=l.comp,
                        val=l.val
                    )
                )
                global_cargo_id += 1

        if not vehicles or not cargos:
            return {
                "error": "Missing trucks or loads to process.",
                "total_value": 0,
                "allocations": []
            }

        # 3. Execute Solver
        result: AllocationResult = self.solver.solve(cargos, vehicles)

        # 4. Process and format results
        return self._format_result(result, cargos, vehicles)

    def _format_result(self, result: AllocationResult, cargos: List[Cargo], vehicles: List[Vehicle]) -> Dict[str, Any]:
        vehicle_map = {v.id: v for v in vehicles}
        
        # Initialize containers for grouped results
        trucks_info = {
            v.id: {
                "truck_id": v.id,
                "nome": v.nome,
                "capacidade_peso": v.cap_peso,
                "peso_utilizado": 0.0,
                "comprimento_total": v.comp,
                "comprimento_utilizado": 0.0,
                "valor_total": 0.0,
                "itens": []
            } for v in vehicles
        }
        
        not_allocated = []

        # Iterate through allocations
        for i, vehicle_id in enumerate(result.allocations):
            cargo = cargos[i]
            if vehicle_id != -1:
                truck = trucks_info[vehicle_id]
                truck["peso_utilizado"] += cargo.peso
                truck["comprimento_utilizado"] += cargo.comp
                truck["valor_total"] += cargo.val
                truck["itens"].append({
                    "id": cargo.id,
                    "nome": cargo.name,
                    "peso": cargo.peso,
                    "comp": cargo.comp,
                    "valor": cargo.val
                })
            else:
                not_allocated.append({
                    "id": cargo.id,
                    "nome": cargo.name,
                    "peso": cargo.peso,
                    "comp": cargo.comp,
                    "valor": cargo.val
                })

        # Calculate percentages and clean up
        final_trucks = []
        for t_id in trucks_info:
            t = trucks_info[t_id]
            t["percentual_peso"] = round((t["peso_utilizado"] / t["capacidade_peso"]) * 100, 2) if t["capacidade_peso"] > 0 else 0
            t["percentual_comprimento"] = round((t["comprimento_utilizado"] / t["comprimento_total"]) * 100, 2) if t["comprimento_total"] > 0 else 0
            final_trucks.append(t)

        return {
            "resumo_geral": {
                "valor_total_alocado": result.total_value,
                "qtd_itens_alocados": sum(len(t["itens"]) for t in final_trucks),
                "qtd_itens_nao_alocados": len(not_allocated),
                "tempo_execucao_segundos": round(result.execution_time, 4),
                "nos_explorados": result.nodes_explored
            },
            "caminhoes": final_trucks,
            "nao_alocados": not_allocated
        }
