class Place:

    def __init__(self, row, column, count, number):
        self.row = row
        self.column = column
        self.population = {}
        self.number = number
        self.count = count
        self.modify = True

        for num in range(count):
            self.population[num + 1] = 0

    def increment_population(self):
        self.population[self.number] += 1

    def __str__(self):
        return str(self.number)

    def debug(self):
        return "["+str(self.row)+","+str(self.column)+"] "+str(self.number)

    def __int__(self):
        return int(self.number)

    def min_population(self):
        temp_number = 1
        temp_number_value = self.population[1]

        for num in range(self.count - 1):
            if self.population[num + 2] < temp_number_value:
                temp_number = num + 2
                temp_number_value = self.population[num + 2]
        return [temp_number, temp_number_value]
