# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 20:37:11 2024

@author: DJBird
"""
from Stack_for_ALGO import Stack
import numpy as np

cubic = np.poly1d([2, 3, 0, 1])
print(cubic)
val = np.polyval(cubic, 2)
print(val)

quad = np.poly1d([1, 0, 1])
der = np.polyder(quad)
tanp = np.polyval(der, 1)
print(tanp)

rStack = Stack()


def prompt():
    entering = True
    p = []
    while entering:
        c = input("Enter the coefficients for your polynomial one at a time and hit Enter when done. For example: If entering x^2-1, enter 1, then 0, then -1, then Enter: ")
        if c == "":
            entering = False
        else:
            c = float(c)
            p.append(c)
    x = float(input("Enter an x1 value: "))
    return x, p


def newton(x, p):
    if rStack.isEmpty() == False:
        if abs(rStack.peek()-x) < 0.001:
            rStack.push(x)
            return
        else:
            func = np.poly1d(p)
            fval = np.polyval(func, x)
            deriv = np.polyder(func)
            dval = np.polyval(deriv, x)
            rStack.push(x)
            newx = x-(fval/dval)
            return newton(newx, p)
    else:
        func = np.poly1d(p)
        fval = np.polyval(func, x)
        deriv = np.polyder(func)
        dval = np.polyval(deriv, x)
        rStack.push(x)
        newx = x-(fval/dval)
        return newton(newx, p)


def roots(p):
    return print("Roots:", np.roots(p))


def main():
    x, p = prompt()
    newton(x, p)
    final = rStack.peek()
    for i in range(rStack.size()):
        print(f"x_{i+1} = {rStack.items[i]:.3f}")
    print(f"The final value with stabilized thousands place is: {final:.3f}")
    roots(p)


main()
