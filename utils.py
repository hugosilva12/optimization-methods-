

INITIAL_PATH = 'input_files/'

OUT_PATH = 'output_files/'

def generate_customers(value: int) -> tuple:
    customers =[]
    for id in range(value):
        customers.append({"customer_id": id })
    return tuple(customers)


def generate_facilities(value: int) -> tuple:
    facilities =  []
    for id in range(value):
        facilities.append({"facility_id": id })
    return tuple(facilities)


def add_total_capacity_on_facilities(values:list[str], facilities_tuple:tuple) -> tuple:
    for index, total_capacity in enumerate(values):
        facilities_tuple[index]["total_capacity"] = int(total_capacity)
    return facilities_tuple


def add_opening_cost_on_facilities(values:list[str], facilities_tuple:tuple) -> tuple:
    for index, opening_cost in enumerate(values):
        facilities_tuple[index]["opening_cost"] = float(opening_cost)
    return facilities_tuple


def add_demand_on_customers(values:list[str], customers_tuple:tuple) -> tuple:
    for index, demand in enumerate(values):
        customers_tuple[index]["demand"] = int(demand)
    return customers_tuple
