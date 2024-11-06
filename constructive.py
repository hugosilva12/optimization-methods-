
"""
   This class contains the constructive heuristics and the local search
"""

import numpy as np
from instance import Instance
from solution import Solution
from facility import Facility
import time
import random
import copy
class Constructive:

    def __init__(self, instance: Instance):
        self.instance = instance

    def solve_construtive_1(self) -> Solution:
        start_time = time.time()
        solution = Solution(self.instance)

        facilities = solution.get_instance().get_facilities()
        customers = solution.get_instance().get_customers()
        served_customers = set()

        while len(served_customers) < len(customers):

            optimal_facility = min(
                filter(lambda f: not f.the_facility_is_open(), facilities),
                key=lambda f: f.get_opening_cost() / (f.get_current_capacity())
            )

            optimal_facility.open()

            for customer in customers:
                if customer.get_chosen_facility_id() == -1 and  customer.get_demand() <= optimal_facility.get_current_capacity() :
                    customer.set_chosen_facility_id(optimal_facility.get_facility_id())
                    optimal_facility.add_customer(customer)
                    served_customers.add(customer)


        return solution


    def solve_construtive_2(self, only_construtive :bool) -> Solution:
        solution = Solution(self.instance)

        facilities = solution.get_instance().get_facilities()
        customers = solution.get_instance().get_customers()
        served_customers = set()

        while len(served_customers) < len(customers):
            open_facilities = [f for f in facilities if not f.the_facility_is_open()]
            optimal_facility = min(open_facilities, key=lambda f: f.get_opening_cost() / f.get_current_capacity())
            optimal_facility.open()

            sorted_customers = list(filter(lambda c: c.get_chosen_facility_id() == -1, solution.get_instance().get_customers()))
            sorted_customers.sort(key=lambda c: c.get_transportation_costs()[optimal_facility.get_facility_id()] / c.get_demand())

            facility_id = optimal_facility.get_facility_id()
            for customer in sorted_customers:
                chosen_facility_id = customer.get_chosen_facility_id()
                customer_demand = customer.get_demand()

                if chosen_facility_id == -1 and customer_demand <= optimal_facility.get_current_capacity():
                    customer.set_chosen_facility_id(facility_id)
                    optimal_facility.add_customer(customer)
                    served_customers.add(customer)



        if only_construtive :
            best_value = solution.get_solution_value()
            return solution
        else:
            improve = True
            best_value = solution.get_solution_value()

            while improve == True:
                improve = False

                optimezed_solution = self.shift_customer(solution)

                optimezed_swap = self.swap_customers(optimezed_solution)

                if optimezed_swap.get_solution_value() < best_value:
                    improve = True
                    solution = copy.deepcopy(optimezed_solution)
                    best_value = optimezed_solution.get_solution_value()

            return solution



    def sort_customers(self,facility, possible_customers):
        global sorted_customer_queue
        sorted_customer_queue = sorted(possible_customers, key=lambda c: c.get_transportation_costs()[facility.get_facility_id()])


    def create_transports_cost_matrix(self,  solution: Solution):
        transportation_costs = {}

        for facility in solution.get_instance().get_facilities():
            facility_id = facility.get_facility_id()
            transportation_costs[facility_id] = {}

            for customer in solution.get_instance().get_customers():
                customer_id = customer.get_customer_id()
                cost = customer.get_transportation_costs()[facility_id]
                transportation_costs[facility_id][customer_id] = cost

        return transportation_costs

    def shift_customer(self, solution: Solution):
        best_solution = copy.deepcopy(solution)
        best_solution_current_value = best_solution.get_solution_value()
        current_solution = copy.deepcopy(best_solution)
        transportation_costs = self.create_transports_cost_matrix(solution)
        improvement = True

        while improvement:
            improvement = False
            for customer in current_solution.get_instance().get_customers():
                current_cost = customer.get_transportation_costs()[customer.get_chosen_facility_id()]
                for facility in current_solution.get_instance().get_facilities():
                    if not facility.can_satisfy_customer(customer):
                        continue

                    cost = transportation_costs[facility.get_facility_id()][customer.get_customer_id()]

                    chosen_facility = current_solution.get_instance().get_facilities()[
                        customer.get_chosen_facility_id()]

                    if len(chosen_facility.get_costumers()) == 1:
                        cost -= chosen_facility.get_opening_cost()

                    if current_cost > cost:
                        chosen_facility.remove_customer(customer)
                        customer.set_chosen_facility_id(facility.get_facility_id())
                        facility.add_customer(customer)

                        current_solution_cost = current_solution.get_solution_value()

                        if len(chosen_facility.get_costumers()) == 0:
                            current_solution_cost -= chosen_facility.get_opening_cost()
                            chosen_facility.close()

                        if current_solution_cost < best_solution_current_value:
                            best_solution = copy.deepcopy(current_solution)
                            best_solution_current_value = current_solution_cost
                            improvement = True
                            break


        return best_solution

    def swap_customers(self, solution: Solution) -> Solution:
        best_solution = copy.deepcopy(solution)
        best_solution_value = solution.get_solution_value()
        count = 0
        for customer_a in solution.get_instance().get_customers():
            for customer_b in solution.get_instance().get_customers():
                if customer_a == customer_b:
                    continue

                facility_a = solution.get_instance().get_facilities()[customer_a.get_chosen_facility_id()]
                facility_b = solution.get_instance().get_facilities()[customer_b.get_chosen_facility_id()]

                if facility_a == facility_b:
                    continue

                if not facility_a.can_swap_customer(customer_a, customer_b) or not facility_b.can_swap_customer(
                        customer_b, customer_a):
                    continue

                temp_solution_value = best_solution_value

                temp_solution_value -= customer_a.get_transportation_costs()[facility_a.get_facility_id()]
                temp_solution_value -= customer_b.get_transportation_costs()[facility_b.get_facility_id()]

                temp_solution_value += customer_b.get_transportation_costs()[facility_a.get_facility_id()]
                temp_solution_value += customer_a.get_transportation_costs()[facility_b.get_facility_id()]

                if temp_solution_value < best_solution_value:
                    facility_a.remove_customer(customer_a)
                    customer_b.set_chosen_facility_id(facility_a.get_facility_id())
                    facility_a.add_customer(customer_b)
                    facility_b.remove_customer(customer_b)
                    customer_a.set_chosen_facility_id(facility_b.get_facility_id())
                    facility_b.add_customer(customer_a)

                    best_solution = copy.deepcopy(solution)
                    best_solution_value = temp_solution_value

                    return best_solution

        return best_solution



