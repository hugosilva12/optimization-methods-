"""
   This class contains the tabu search metaheuristic
"""
from instance import Instance
from solution import Solution
from facility import Facility
import copy
from tabu_memory import TabuMemory
from typing import List, Tuple
from customer import Customer
import random
import itertools


class TabuSearch:
    def __init__(self, initial_solution: Solution, tabu_size: int, max_iterations: int):
        self.initial_solution = initial_solution
        self.tabu_size = tabu_size
        self.max_iterations = max_iterations
        self.tabu_list = TabuMemory(tabu_size)
        self.use_diversification= True


    def run(self) -> Solution:
        current_solution = self.initial_solution
        best_solution = self.initial_solution
        current_best_solution_value = best_solution.get_solution_value()
        previous_best_value = copy.deepcopy(current_best_solution_value)
        count = 0
        iteration = 0
        diversification_start = int(self.max_iterations * 0.7)  # limite de iterações para aplicar a diversificação

        while iteration < self.max_iterations:

              current_solution,changed_solution = self.shift_customer(current_solution, iteration, current_best_solution_value)
              current_solution_value = current_solution.get_solution_value()

              if current_solution_value <  current_best_solution_value:
                  previous_best_value  = copy.deepcopy(current_solution_value)
                  best_solution = copy.deepcopy(current_solution)
                  current_best_solution_value = copy.deepcopy(current_solution_value)

              swap_solution = self.swap_customer(current_solution)
              swap_solution_value = swap_solution.get_solution_value()

              if swap_solution_value < current_best_solution_value:
                  best_solution = copy.deepcopy(swap_solution)
                  current_best_solution_value = copy.deepcopy(swap_solution_value)


              elif not changed_solution and iteration >= diversification_start and  self.use_diversification:
                  current_solution = self.diversify_solution(current_solution)

                  diversification_solution_value = current_solution.get_solution_value()
                  if diversification_solution_value < current_best_solution_value:
                      best_solution = copy.deepcopy(current_solution)
                      current_best_solution_value = diversification_solution_value

              iteration += 1

        return best_solution

    def diversify_solution(self, solution: Solution) -> Solution:

        for customer in solution.get_instance().get_customers():
            current_facility_id = customer.get_chosen_facility_id()

            available_facilities = []
            for facility in  solution.get_instance().get_facilities():

                if facility.can_satisfy_customer(customer):
                    available_facilities.append(facility)

            if len(available_facilities) > 0:
                random_facility = random.choice(available_facilities)
                random_facility_id = random_facility.get_facility_id()

                if current_facility_id != random_facility_id:
                    current_facility = solution.get_instance().get_facilities()[current_facility_id]

                    current_facility.remove_customer(customer)
                    if len(current_facility.get_costumers()) == 0:
                        current_facility.close()

                    customer.set_chosen_facility_id(random_facility_id)
                    random_facility.add_customer(customer)

        return solution


    def create_transports_cost_matrix(self, solution: Solution):
        transportation_costs = {}

        for facility in solution.get_instance().get_facilities():
            facility_id = facility.get_facility_id()
            transportation_costs[facility_id] = {}

            for customer in solution.get_instance().get_customers():
                customer_id = customer.get_customer_id()
                cost = customer.get_transportation_costs()[facility_id]
                transportation_costs[facility_id][customer_id] = cost

        return transportation_costs

    def shift_customer(self, solution: Solution, iteration:int, current_best_solution_value:int):
        best_solution_current_value = solution.get_solution_value()
        current_solution = copy.deepcopy(solution)
        transportation_costs = self.create_transports_cost_matrix(solution)
        improvement = True
        count = 0

        while improvement:
          improvement = False
          for customer in current_solution.get_instance().get_customers():

            current_cost = customer.get_transportation_costs()[customer.get_chosen_facility_id()]
            for facility in current_solution.get_instance().get_facilities():

                if not facility.can_satisfy_customer(customer):
                    continue

                new_cost = transportation_costs[facility.get_facility_id()][customer.get_customer_id()]

                chosen_facility = current_solution.get_instance().get_facilities()[
                    customer.get_chosen_facility_id()]

                if len(chosen_facility.get_costumers()) == 1:
                    new_cost -= chosen_facility.get_opening_cost()


                ## Criterio de aceitação
                is_tabu_move = self.is_tabu_move(customer.get_customer_id(),facility.get_facility_id())

                if current_cost >= new_cost:
                    bestValue =  best_solution_current_value + (new_cost - current_cost)

                    if len(chosen_facility.get_costumers()) == 1:
                        bestValue -= chosen_facility.get_opening_cost()

                    if current_best_solution_value > bestValue:
                        is_tabu_move = False


                if current_cost > new_cost and not is_tabu_move:
                    chosen_facility.remove_customer(customer)
                    customer.set_chosen_facility_id(facility.get_facility_id())
                    facility.add_customer(customer)

                    if len(chosen_facility.get_costumers()) == 0:
                        chosen_facility.close()

                    improvement = True
                    count = 1
                    self.update_tabu_list(customer.get_customer_id(), facility.get_facility_id())
                    break

        if count == 1:
            return current_solution , True
        else:
            return self.local_search_for_worse(current_solution)

    def local_search_for_worse(self, solution: Solution):
        current_solution = solution
        transportation_costs = self.create_transports_cost_matrix(solution)
        change = ()
        min_cust = -1
        for customer in current_solution.get_instance().get_customers():
            current_cost = customer.get_transportation_costs()[customer.get_chosen_facility_id()]
            for facility in current_solution.get_instance().get_facilities():
                if not facility.can_satisfy_customer(customer):
                    continue

                new_cost = transportation_costs[facility.get_facility_id()][customer.get_customer_id()]

                chosen_facility = current_solution.get_instance().get_facilities()[
                    customer.get_chosen_facility_id()]

                if len(chosen_facility.get_costumers()) == 1:
                    new_cost -= chosen_facility.get_opening_cost()

                if self.is_tabu_move(customer.get_customer_id(), facility.get_facility_id()):
                    continue

                min_cust_op = new_cost - current_cost

                if min_cust == -1:
                    min_cust = min_cust_op
                    change = (customer.get_customer_id(), facility.get_facility_id())
                elif min_cust_op < min_cust:
                    min_cust = min_cust_op
                    change = (customer.get_customer_id(), facility.get_facility_id())

        if change != ():
            customer_id, facility_id = change
            customer = current_solution.get_instance().get_customers()[customer_id]
            chosen_facility = current_solution.get_instance().get_facilities()[
                customer.get_chosen_facility_id()]

            facility = current_solution.get_instance().get_facilities()[
                facility_id]

            chosen_facility.remove_customer(customer)
            customer.set_chosen_facility_id(facility.get_facility_id())
            facility.add_customer(customer)

            self.update_tabu_list(customer.get_customer_id(), facility.get_facility_id())

            if len(chosen_facility.get_costumers()) == 0:
                chosen_facility.close()

        return current_solution, change != ()


    def swap_customer(self, solution: Solution) -> Solution:
        best_solution_value = solution.get_solution_value()
        count = 0
        min_cust = -1
        swap_a = ()
        swap_b = ()

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

                ## Criterio de aceitação
                is_tabu_move = self.is_tabu_move(customer_a.get_customer_id(), facility_b.get_facility_id()) and  self.is_tabu_move(customer_b.get_customer_id(), facility_a.get_facility_id())
                temp_solution_value = best_solution_value

                temp_solution_value -= customer_a.get_transportation_costs()[facility_a.get_facility_id()]
                temp_solution_value -= customer_b.get_transportation_costs()[facility_b.get_facility_id()]

                temp_solution_value += customer_b.get_transportation_costs()[facility_a.get_facility_id()]
                temp_solution_value += customer_a.get_transportation_costs()[facility_b.get_facility_id()]


                if temp_solution_value < best_solution_value :

                    facility_a.remove_customer(customer_a)
                    customer_b.set_chosen_facility_id(facility_a.get_facility_id())
                    facility_a.add_customer(customer_b)
                    facility_b.remove_customer(customer_b)
                    customer_a.set_chosen_facility_id(facility_b.get_facility_id())
                    facility_b.add_customer(customer_a)

                    self.update_tabu_list(customer_a.get_customer_id(), facility_b.get_facility_id())
                    self.update_tabu_list(customer_b.get_customer_id(), facility_a.get_facility_id())
                    return solution


                elif min_cust == -1 and temp_solution_value > 0 and not is_tabu_move:
                    min_cust = temp_solution_value
                    swap_a = (customer_a.get_customer_id(), facility_b.get_facility_id())
                    swap_b = (customer_b.get_customer_id(), facility_a.get_facility_id())

                elif temp_solution_value < min_cust and temp_solution_value > 0 and not is_tabu_move:
                    min_cust = temp_solution_value
                    swap_a = (customer_a.get_customer_id(), facility_b.get_facility_id())
                    swap_b = (customer_b.get_customer_id(), facility_a.get_facility_id())

        if swap_a != ():
            customer_a_id, facility_b_id = swap_a
            customer_b_id, facility_a_id = swap_b

            customer_a = solution.get_instance().get_customers()[customer_a_id]
            customer_b = solution.get_instance().get_customers()[customer_b_id]

            facility_a = solution.get_instance().get_facilities()[facility_a_id]
            facility_b = solution.get_instance().get_facilities()[facility_b_id]

            facility_a.remove_customer(customer_a)
            customer_b.set_chosen_facility_id(facility_a.get_facility_id())
            facility_a.add_customer(customer_b)
            facility_b.remove_customer(customer_b)
            customer_a.set_chosen_facility_id(facility_b.get_facility_id())
            facility_b.add_customer(customer_a)

            self.update_tabu_list(customer_a.get_customer_id(), facility_b.get_facility_id())
            self.update_tabu_list(customer_b.get_customer_id(), facility_a.get_facility_id())

        return solution
    def update_tabu_list(self, customer_id, facility_id):
        self.tabu_list.add(customer_id, facility_id)

    def is_tabu_move(self, customer_id, facility_id):
        return self.tabu_list.is_tabu_move(customer_id, facility_id)

