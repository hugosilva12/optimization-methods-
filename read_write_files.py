"""
    This file contains all the methods needed to create an instance of the problem using the provided datasets
"""
import os
from utils import OUT_PATH,generate_customers,generate_facilities,add_total_capacity_on_facilities,add_opening_cost_on_facilities,add_demand_on_customers
from customer import Customer
from instance import Instance
from facility import Facility
from transportation_costs import TransportationCosts

def sort_by_number(filename):
    number = ""
    for character in filename:
        if character.isdigit():
            number += character
    return int(number)


def get_all_folders_of_a_directory(filename: str) -> list:
    folders = []
    try:
        for path in os.listdir(filename):
            if os.path.isdir(os.path.join(filename, path)) :
                folders.append(path)
        folders = sorted(folders, key=sort_by_number)
    except Exception as e:
        print("Error " + str(e))
    return folders


def get_all_files_of_a_directory(filename: str) -> list:
    files = []
    try:
        for path in os.listdir(filename):
            if os.path.isfile(os.path.join(filename, path)) and path != 'os':
                files.append(path)
        files = sorted(files, key=sort_by_number)
    except Exception as e:
        print("Error " + str(e))
    return files

# obtain transport costs from each customer to the facilities
def get_transport_costs_by_customer_id(customer_id:int,matrix_with_the_transportation_cost: [TransportationCosts])-> [float]:
    for transport_cost in matrix_with_the_transportation_cost:
        if transport_cost.get_customer_id() == customer_id:
            return transport_cost.get_transportation_costs()

def instance_customers(customers_from_file: tuple, matrix_with_the_transportation_cost: [TransportationCosts]) -> tuple:
    customers = []
    for customer_from_file in customers_from_file:
        customers.append(Customer(customer_from_file["customer_id"], customer_from_file["demand"],get_transport_costs_by_customer_id(customer_from_file["customer_id"],matrix_with_the_transportation_cost)))
    return tuple(customers)

def instance_facilities(facilities_from_file: tuple) -> tuple:
    facilities = []
    for facility in facilities_from_file:
        facilities.append(Facility(facility["facility_id"], facility["opening_cost"],facility["total_capacity"]))

    return tuple(facilities)


def create_instance_from_a_file(filename: str) -> Instance:
    customers={}
    facilities ={}
    matrix_with_the_transportation_cost = []
    customer_id = 0
    with open(filename, "r") as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            line_formatted = line.strip().split(" ")
            try:
              if index == 0: # facilities (I) #customers (J)
                  customers = generate_customers(int(line_formatted[1]))
                  facilities = generate_facilities(int(line_formatted[0]))

              elif index == 1: # row with facilities capacity (I columns)
                  facilities = add_total_capacity_on_facilities(line_formatted, facilities)

              elif index == 2:  # row with facilities opening cost (I columns)
                  facilities = add_opening_cost_on_facilities(line_formatted, facilities)

              elif index == 3:  # row with customers demand (J columns)
                  customers = add_demand_on_customers(line_formatted, customers)

              else: # matrix with the transportation cost between customer and facility (J rows with I columns)
                  matrix_with_the_transportation_cost.append(TransportationCosts(customer_id,(tuple([float(s) for s in line_formatted]))))
                  customer_id = customer_id+1

            except Exception as e:
                    print("Error " + str(e))

    final_costumers_structure = instance_customers(customers,matrix_with_the_transportation_cost)
    final_facilities__structure = instance_facilities(facilities)

    return Instance(final_costumers_structure,final_facilities__structure)



def write_file(filename:str, content:list):
    file = open(OUT_PATH + filename, 'w')
    for c in content:
        file.write(c + "\n")
    file.close