from qubots.base_problem import BaseProblem
import random
import sys
import os

def read_elem(filename):

    # Resolve relative path with respect to this module’s directory.
    if not os.path.isabs(filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(base_dir, filename)


    with open(filename) as f:
        return [str(elem) for elem in f.read().split()]

def read_instance(filename):
    file_it = iter(read_elem(filename))
    # The first number in the second line gives the number of orders _excluding_ the depot.
    nb_orders = int(next(file_it)) + 1
    distances_data = []
    for i in range(nb_orders):
        row = []
        for j in range(nb_orders):
            row.append(int(next(file_it)))
        distances_data.append(row)
    return nb_orders, distances_data

class OrderPickingProblem(BaseProblem):
    """
    Order Picking Problem for Qubots.
    
    Given a distance matrix between orders in a warehouse (including the initial depot at index 0),
    the goal is to determine a picking order (a permutation of the orders) that minimizes the total travel
    distance. The total distance is computed as the sum of the distances between successive orders along the
    route, plus the distance from the last order back to the depot.
    """
    
    def __init__(self, instance_file: str, **kwargs):
        self.nb_orders, self.distances_data = read_instance(instance_file)
    
    def evaluate_solution(self, solution) -> int:
        """
        Evaluates a candidate picking order.
        
        Expects:
          solution: a list of integers (a permutation of 0,...,nb_orders-1) representing the picking order.
          
        Returns:
          The total travel distance along the route (including the return to the depot).
          If the solution is not a permutation of the required size, returns a high penalty.
        """
        if not isinstance(solution, list) or len(solution) != self.nb_orders:
            return sys.maxsize
        if sorted(solution) != list(range(self.nb_orders)):
            return sys.maxsize
        total_distance = 0
        for i in range(self.nb_orders - 1):
            total_distance += self.distances_data[solution[i]][solution[i+1]]
        total_distance += self.distances_data[solution[-1]][solution[0]]
        return total_distance
    
    def random_solution(self):
        """
        Generates a random picking order.
        """
        order = list(range(self.nb_orders))
        random.shuffle(order)
        return order
