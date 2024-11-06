class TabuMemory:
    def __init__(self, tabu_size):
        self.tabu_size = tabu_size
        self.tabu_set = set()

    def add(self, customer_id, facility_id):
        self.tabu_set.add((customer_id, facility_id))
        if len(self.tabu_set) > self.tabu_size:
            self.tabu_set.pop()

    def is_tabu_move(self, customer_id, facility_id):
        return (customer_id, facility_id) in self.tabu_set


