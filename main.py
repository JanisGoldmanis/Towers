import copy

import DrawBoard
import EstimateSolution
import Place
import random

# https://puzzlemadness.co.uk/towers/large/2022/10/19

print_generations = False

left_row = [2,3,3,5,1]
top_row = [2,1,2,3,3]
right_row = [2,3,2,1,4]
bottom_row = [1,5,2,3,2]

# left_row = [0, 4, 0, 0, 2]
# top_row = [3, 0, 4, 3, 2]
# right_row = [2, 1, 5, 2, 0]
# bottom_row = [2, 0, 0, 0, 0]

# left_row = [3,3,3,2,2,4,4,1,3]
# top_row = [4,3,4,2,1,3,4,5,2]
# right_row = [2,4,1,4,5,3,2,4,3]
# bottom_row = [2,2,3,4,6,3,1,2,3]

n = len(left_row)

task = [n, top_row, right_row, bottom_row, left_row]

debug = False



def generate_solution():
    """

    :rtype: list of lists with place objects
    """
    current_solution = []
    for row_index in range(n):
        row = []
        for column_index in range(n):
            piece = Place.Place(row_index + 1, column_index + 1, n, column_index + 1)
            row.append(piece)
        current_solution.append(row)
    return current_solution


def add_population(solution):
    for row in solution:
        for place in row:
            place.increment_population()


def create_solution_copy(solution):
    temp_solution = []
    for row in solution:
        temp_row = copy.deepcopy(row)
        temp_solution.append(temp_row)
    return temp_solution


def move_cell(row, index1, index2,debug=False):
    if row[index1].modify == False or row[index2] == False:
        if debug:
            print('Locked, not moving')
        pass
    else:
        row[index1].number, row[index2].number = row[index2].number, row[index1].number


def generate_destinations(origin, n):
    destinations = []
    for number in range(n):
        if number != origin:
            destinations.append(number)
    return destinations


def find_min_population(solution,debug=False):
    temp_place = solution[0][0]
    for row in solution:
        for place in row:
            if debug:
                print('Temp Place:',(temp_place.min_population())[1])
                print('Checking:',(place.min_population())[1])

            if (temp_place.min_population())[1] > (place.min_population())[1]:
                temp_place = place
                if debug:
                    print('Changing min temp place')
    return temp_place


def mutate_solution_to_most_unused_value(current_solution,debug=False):
    temp_place = find_min_population(current_solution)
    row = temp_place.row-1
    column = temp_place.column-1
    number_to_assign = temp_place.min_population()[0]
    current_number = temp_place.number
    for place in current_solution[row]:
        if place.number == number_to_assign:
            place.number = current_number
            break
    temp_place.modify = False
    find_min_population(current_solution).number = find_min_population(current_solution).min_population()[0]
    if debug:
        print('Mutating ',temp_place.debug())
    pass


def unlock_all_cells(current_solution):
    for row in current_solution:
        for place in row:
            place.modify = True


# Generate initial solution and add population to places

current_solution = generate_solution()
add_population(current_solution)

print("Starting solution")
DrawBoard.draw_board(task, current_solution)
print("Solution cost:", EstimateSolution.estimate_solution(task, current_solution, debug=False))

generation_cost = EstimateSolution.estimate_solution(task, current_solution, debug=False)

without_improvement = 0

mutation_flag = False


global_minimum = create_solution_copy(current_solution)
global_best_cost = EstimateSolution.estimate_solution(task, global_minimum)

for iteration in range(15000):
    # Which row
    row = iteration % n
    best_cost = generation_cost
    best_origin = 0
    best_destination = 0

    if debug:
        print()
        print('Iteration:',iteration)
        print('Starting best cost:',best_cost)


    for origin in range(n):
        destinations = generate_destinations(origin, n)

        for destination in destinations:

            if debug:
                print('Checking row',row,'from',origin+1,'to',destination+1)

            temp_solution = create_solution_copy(current_solution)

            move_cell(temp_solution[row], origin, destination)
            current_cost = EstimateSolution.estimate_solution(task, temp_solution)

            if debug:
                print('Best cost',generation_cost,'current cost',current_cost,'difference',generation_cost-current_cost)

            if current_cost < best_cost:
                without_improvement = 0
            if current_cost<= best_cost:
                best_origin = origin
                best_destination = destination
                best_cost = current_cost

    if debug:
        print('Generation best move - row',row,'origin',best_origin+1,'destination',best_destination+1)

    move_cell(current_solution[row], best_origin, best_destination)
    generation_cost = best_cost

    if without_improvement > 2 * n:
        if mutation_flag:
            unlock_all_cells(current_solution)
            without_improvement = 0
            mutation_flag = False
        else:
        # row = random.randint(0, n - 1)
        # column1 = random.randint(0, n - 1)
        # column2 = generate_destinations(column1, n)[random.randint(0, n - 2)]
        # move_cell(current_solution[row], column1, column2)

            print("Mutating solution, generation:", iteration)
            mutate_solution_to_most_unused_value(current_solution,debug=True)
            without_improvement = 0
            mutation_flag = True

    if print_generations:
        DrawBoard.draw_board(task, current_solution)
        print("Solution cost:", EstimateSolution.estimate_solution(task, current_solution),"Generation:",iteration)

    without_improvement += 1
    if EstimateSolution.estimate_solution(task, current_solution) == 0:
        print("Perfect solution achieved")
        global_best_cost = EstimateSolution.estimate_solution(task, current_solution)
        global_minimum = current_solution
        break

    if global_best_cost > best_cost:
        global_minimum = create_solution_copy(current_solution)

    add_population(current_solution)

DrawBoard.draw_board(task, global_minimum)
print("Solution cost:", EstimateSolution.estimate_solution(task, global_minimum))

print("Generations:", iteration+1)

# print(current_solution[0][0].population)
# print(current_solution[0][0].min_population())
# print(current_solution[1][1].population)
# print(current_solution[1][1].min_population())
#
# print(find_min_population(current_solution, False).debug())