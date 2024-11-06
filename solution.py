
from typing import List
from customer import Customer
from instance import Instance
from facility import Facility

class Solution:
    # 'instance' - instância do problema que estamos resolvendo
    # 'facilities' - lista de instalações em que estamos interessados
    # 'served_customers' - lista de clientes que já foram atendidos por alguma instalação
    # 'assigned_facilities' - lista de instalações a que cada cliente foi atribuído

    def __init__(self, instance: Instance):
        self.instance = instance
        self.solution_value = -1

    def get_instance(self) -> Instance:
        return self.instance

    def get_facilities(self) -> List[Facility]:
        return self.instance.facilities

    def get_customers(self) -> List[Customer]:
        return self.instance.customers


    def get_open_facilities(self) -> List[Facility]:
        return [facility for facility in self.instance.get_facilities() if facility.the_facility_is_open()]
    def get_solution_value(self) -> float:
        return sum((facility.get_total_cost() if facility.the_facility_is_open() else 0 for facility in
                    self.instance.get_facilities()))

    def print_solution_details(self):
        print("Solution Details:")
        print("Instance: ", self.instance)
        print("Facilities: ", [facility.get_facility_id() for facility in self.instance.facilities])
        print("Facilities Capacity: ", [facility.get_current_capacity() for facility in self.instance.facilities])
        print("Facilities Open: ", [facility.the_facility_is_open() for facility in self.instance.facilities])
        print("Served Customers: ", [customer.get_customer_id() for customer in self.instance.customers if
                                     customer.get_chosen_facility_id() != -1])


        print("Assigned Facilities:")
        for customer in self.instance.customers:
            facility_id = customer.get_chosen_facility_id()
            if facility_id != -1:
                print("Customer ", customer.get_customer_id() + 1, " assigned to Facility ", facility_id + 1)


