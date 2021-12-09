a = (a*4+1 for a in range(0, 11))  # Seat no. generator
seats = []  # Seats in a compartment

for i in range(11):
    seats.append(next(a))

try:
    compartment = int(input())
    if compartment in range(0, 11):
        for i in range(0, 4):
            print(seats[compartment-1]+i)  # Seats in specified compartment
        print(seats[10]+4 + (11-compartment)*2, seats[10]+4 + (11-compartment)*2 + 1)  # Seats in front of specified compartment
except:
    print("error")