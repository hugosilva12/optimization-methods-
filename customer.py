
"""
   This class has the function of storing the data of a customer
"""
class Customer:
    # 'customer_id' - pode ser preciso, identifica o cliente
    # 'demand' - o que ele procura
    #  'demand_satisfied' - variavel que indica  se a procura está satisfeita, começa sempre a false

    def __init__(self, customer_id:int, demand: int, transportation_costs:[float]):
        self.demand = demand
        self.customer_id = customer_id
        self.demand_satisfied = False
        self.transportation_costs = transportation_costs
        self.chosen_facility_id = -1

    def set_chosen_facility_id(self, facility_id:int) -> int:
         self.chosen_facility_id = facility_id

    def get_chosen_facility_id(self) -> int:
        return self.chosen_facility_id

    def get_demand(self) -> int:
        return self.demand

    def get_customer_id(self) -> int:
        return self.customer_id

    def get_demand_satisfied(self) -> bool:
        return self.demand_satisfied

    def get_transportation_costs(self) -> list:
        return self.transportation_costs

    def unsatisfy(self):
        self.demand_satisfied = False

    def satisfy(self):
        self.demand_satisfied = True

    def __str__(self):
        return f"Customer(customer_id={self.customer_id}, demand={self.demand}, demand_satisfied={self.demand_satisfied}, transportation_costs={self.transportation_costs})"