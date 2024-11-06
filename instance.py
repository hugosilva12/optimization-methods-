"""
   This class has the function of storing an instance of the problem
"""
class Instance:

    def __init__(self, customers: tuple, facilities: tuple):
        self.customers = customers
        self.facilities = facilities

    def get_customers(self) -> tuple:
        return self.customers

    def get_facilities(self) -> tuple:
        return self.facilities

    def get_transportation_costs_matrix(self) -> tuple:
        return [customer.get_transportation_costs() for customer in self.customers]
