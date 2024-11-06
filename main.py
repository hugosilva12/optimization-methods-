
from read_write_files import get_all_files_of_a_directory,get_all_folders_of_a_directory,write_file,create_instance_from_a_file
from utils import INITIAL_PATH
from constructive import Constructive
from copy import deepcopy
from time import perf_counter
import os
from tabu_search import TabuSearch
def execute_algorithm(lib_name :str):
    files = get_all_files_of_a_directory(INITIAL_PATH + lib_name)
    constructive_file = open(f"out/{lib_name.replace('/','')}.txt", "w")
    constructive_file.write("File | Time | Solution\n")
    for file in files:
        instance = create_instance_from_a_file(INITIAL_PATH + lib_name + file)
        greedy = Constructive(instance)

        time_constructive_start = perf_counter()
        constructive_solution = greedy.solve_construtive_2(True)
        solver = TabuSearch(constructive_solution, 20, 300)
        tabu_search_solution = solver.run()
        time_constructive_end = perf_counter()
        time_taken_constructive = time_constructive_end - time_constructive_start

        constructive_file.write(f"{file} | "
                                f"{time_taken_constructive * 1000}ms |"
                                f" {round(tabu_search_solution.get_solution_value(), 2)}\n")


    constructive_file.close()

if __name__ == '__main__':
        execute_algorithm('Lib_1/')

