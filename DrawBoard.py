def draw_board(task, solution):
    result = []

    # First row
    row = " "
    for num in task[1]:
        row += "  " + str(num)
    result.append(row)

    # Middle rows
    for num in range(len(solution)):
        row = ""
        row += str(task[4][num]) + " "
        for number in solution[num]:
            row += "[" + str(number) + "]"
        row += " " + str(task[2][num])
        result.append(row)

    # Last row
    row = " "
    for num in task[3]:
        row += "  " + str(num)
    result.append(row)

    for row in result:
        print(row)
