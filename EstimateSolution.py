def estimate_solution(task, solution, debug=False):
    # Checking Task vs Solution
    cost = 0

    # Number of rows
    n = task[0]

    # power of difference times 10
    modifier = 2

    if debug:
        print("Puzzle size:", n)

    # Checking how many towers are visible against each task nr
    # First tower next to specific task nr gets assigned as default
    # and then it's compared against each next tower on particular axis and direction

    # Top row, checking from top to bottom
    top_row = task[1]
    if debug:
        print("Top Task", top_row)
    for column in range(n):
        if top_row[column] != 0:
            visible = 1
            highest_tower = solution[0][column].number
            for row in range(n - 1):
                if solution[row + 1][column].number > highest_tower:
                    visible += 1
                    highest_tower = solution[row + 1][column].number
            if debug:
                print("Task:", top_row[column], "Visible", visible, "Cost", abs((top_row[column] - visible)*10) ** modifier)
            cost += abs((top_row[column] - visible)*10) ** modifier

    # Bottom row, checking from bottom to top
    bottom_row = task[3]
    if debug:
        print("Bottom Task", bottom_row)
    for column in range(n):
        if bottom_row[column] != 0:
            visible = 1
            highest_tower = solution[n - 1][column].number
            for row in range(n - 1):
                if solution[n - row - 1 - 1][column].number > highest_tower:
                    visible += 1
                    highest_tower = solution[n - row - 1 - 1][column].number
            if debug:
                print("Task:", bottom_row[column], "Visible", visible, "Cost",
                      abs((bottom_row[column] - visible)*10) ** modifier)
            cost += abs((bottom_row[column] - visible)*10) ** modifier

    # Left side, checking from left to right
    left_side = task[4]
    if debug:
        print("Left Task", left_side)
    for row in range(n):
        if left_side[row] != 0:
            visible = 1
            highest_tower = solution[row][0].number
            for column in range(n - 1):
                if solution[row][column + 1].number > highest_tower:
                    visible += 1
                    highest_tower = solution[row][column + 1].number
            if debug:
                print("Task", left_side[row], "Visible", visible, "Cost", abs((left_side[row] - visible)*10) ** modifier)
            cost += abs((left_side[row] - visible)*10) ** modifier

    # Right side
    right_side = task[2]
    if debug:
        print("Right Task", right_side)
    for row in range(n):
        if right_side[row] != 0:
            visible = 1
            highest_tower = solution[row][n - 1].number
            for column in range(n - 1):
                if solution[row][n - 1 - column - 1].number > highest_tower:
                    visible += 1
                    highest_tower = solution[row][n - 1 - column - 1].number
            if debug:
                print("Task", right_side[row], "Visible", visible, "Cost", abs((right_side[row] - visible)*10) ** modifier)
            cost += abs((right_side[row] - visible)*10) ** modifier

    # Checking columns for equal numbers
    for column in range(n):
        dictionary = {}
        for num in range(n):
            dictionary[num + 1] = 0
        for row in range(n):
            dictionary[solution[row][column].number] += 1
        if debug:
            print(dictionary)

        for number in range(n):
            if dictionary[number + 1] != 1:
                cost += dictionary[number + 1]
            if dictionary[number + 1] == 0:
                cost += 5

    return cost
