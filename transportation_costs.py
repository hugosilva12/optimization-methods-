

"""
    This class has the function of storing the transport costs between a customer and all facilities
"""
class TransportationCosts:
    # 'customer_id' -  identifica o cliente
    # 'Transportation_costs' - custo de transporte para cada Facility

    def __init__(self, customer_id:int, transportation_costs: [float]):
        self.customer_id = customer_id
        self.transportation_costs = transportation_costs


    def get_customer_id(self):
        return self.customer_id


    def get_transportation_costs(self):
        return self.transportation_costs