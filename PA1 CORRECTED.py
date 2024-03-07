# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:33:39 2024

@author: DJBird
"""
import random
import time
from tabulate import tabulate

# Your code to be timed

def one_dimension(moves):
    x = 0
    counter = 0
    for i in range(moves):
        direction=random.choice(["left", "right"])
        if direction == "left":
            x -= 1
        elif direction =="right":
            x += 1
        if x == 0:
            counter += 1
            break
    return counter

def two_dimensions(moves):
    x = 0
    y = 0
    counter = 0
    for i in range(moves):
        direction=random.choice(["left", "right", "up", "down"])
        if direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
        elif direction == "down":
            y -= 1
        elif direction == "up":
            y += 1
        if x == 0 and y == 0:
            counter += 1
            break
    return counter

def three_dimensions(moves):
    x = 0
    y = 0
    z = 0
    counter = 0
    for i in range(moves):
        direction=random.choice(["left", "right", "up", "down", "in", "out"])
        if direction == "left":
            x -= 1
        elif direction == "right":
            x += 1
        elif direction == "down":
            y -= 1
        elif direction == "up":
            y += 1
        elif direction == "in":
            z -= 1
        elif direction == "out":
            z += 1
        if x == 0 and y == 0 and z == 0:
            counter += 1
            break
    return counter

def main():
    move_values=[20, 200, 2000, 20000, 200000, 2000000]
    one_d=[]
    two_d=[]
    three_d=[]
    times=[]
    for move in move_values:
        start_time = time.time()
        final_count1 = 0
        final_count2 = 0
        final_count3 = 0
        for i in range(100):
            final_count1 += one_dimension(move)
            final_count2 += two_dimensions(move)
            final_count3 += three_dimensions(move)
        one_d.append(final_count1)
        two_d.append(final_count2)
        three_d.append(final_count3)
        end_time = time.time()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
          
    print("Percentage of time particle returned to origin:")
    # Sample data
    data = [
        ["1D", one_d[0], one_d[1], one_d[2], one_d[3], one_d[4], one_d[5]],
        ["2D", two_d[0], two_d[1], two_d[2], two_d[3], two_d[4], two_d[5]],
        ["3D", three_d[0], three_d[1], three_d[2], three_d[3], three_d[4], three_d[5]],
    ]
    
    # Table headers
    headers = ["Number of steps:", "20", "200",
                "2,000", "20,000", "200,000",
                "2,000,000"]
    
    # Use the tabulate function to format the data into a table
    table = tabulate(data, headers, tablefmt="grid")
    
    # Print the formatted table
    print(table)
    print()
    # Calculate and print the elapsed time and total
    print("Run time (seconds):")
    print("Number of steps:    20      200      2,000      20,000      200,000      2,000,000")
    print(f"3D                {times[0]:.2f}     {times[1]:.2f}       {times[2]:.2f}        {times[3]:.2f}         {times[4]:.2f}          {times[5]:.2f}")
    
main()



    

            

