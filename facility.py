
from exceptions.facility_not_empty_exception import FacilityNotEmptyException
from exceptions.facility_not_serve_customer_exception import FacilityCannotServeCustomerException
from customer import Customer
from typing import List, Set
"""
    This class has the function of storing the data of a facility
"""
class Facility:

    # 'facility_id' - identifica o facility
    # 'opening_cost' - custo fixo do facility
    # 'total_capacity' - capacidade que ele tem inicialmente
    # 'current_capacity' - guarda o valor da capacidade 'atualizado'
    # 'is_open' - esta aberta
    # 'customers' - lista de clientes
    def __init__(self, facility_id: int, opening_cost: float, total_capacity:float):
        self.opening_cost = opening_cost
        self.facility_id = facility_id
        self.total_capacity = total_capacity
        self.current_capacity = total_capacity
        self.is_open = False
        self.customers = set()

    def add_customer(self, customer: Customer):
        if self.current_capacity >= customer.get_demand():
            self.current_capacity -= customer.get_demand()
            customer.satisfy()
            self.customers.add(customer)
            self.is_open = True
            return True
        else:
            raise FacilityCannotServeCustomerException(self.facility_id, customer.get_customer_id())

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        if len(self.customers) > 0:
            raise FacilityNotEmptyException(self.facility_id)
        self.is_open = False

    def get_facility_id(self) -> int:
        return self.facility_id


    def get_total_capacity(self) -> int:
        return self.total_capacity

    def get_current_capacity(self) -> int:
        return self.current_capacity

    def get_opening_cost(self) -> float:
        return self.opening_cost

    def the_facility_is_open(self) -> bool:
        return self.is_open

    def get_total_cost(self) -> float:
        if not self.the_facility_is_open():
            return 0
        return self.opening_cost + sum((customer.get_transportation_costs()[self.facility_id]
                                          for customer in self.customers))

    def get_costumers(self) ->  Set[Customer]:
        return  self.customers

    def remove_customer(self, customer: Customer) -> None:
        customer.unsatisfy()
        if customer in self.customers:
            self.customers.remove(customer)
            self.current_capacity += customer.get_demand()


    def can_satisfy_customer(self, customer: Customer) -> bool:
        if not self.the_facility_is_open() or customer in self.customers or customer.get_demand() > self.current_capacity:
            return False
        return True

    def can_swap_customer(self, customer_a: Customer, customer_b: Customer) -> bool:
        if not self.the_facility_is_open():
            return False

        if customer_a in self.customers and customer_b not in self.customers:
            new_capacity = self.current_capacity + (customer_a.get_demand() - customer_b.get_demand())
            return new_capacity >= 0
        return False


    def __str__(self) -> str:
        return f"Facility ID: {self.facility_id}\nOpening Cost: {self.opening_cost}\nTotal Capacity: {self.total_capacity}\nCurrent Capacity: {self.current_capacity}"