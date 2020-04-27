from math import sin

def quadratic(a, b, c, t):
    return a*t*t+b*t+c

def sine(a, h, k, x):
    return a*sin(x-h)+k

def my_fun(t):
    return quadratic(1, 2, 4, t) * sine(1, 2, 3, t)