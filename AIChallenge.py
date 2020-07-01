#!/usr/bin/env python
# coding: utf-8

# The python code should have the following components
# 
# a. Code must follow Object Oriented program standards with appropriate Unit tests
# 
# b. Function to generate the initial population
# 
# c. Function to score the population
# 
# d. Function to do cross over and mutation of the selected gene pool
# 
# e. Main function to identify the right sequence

# In[4]:


# 8 Queens puzzle solutions using genetic algorithm

import random
from scipy.special import comb
from numpy import argmax

def chromosome(minimum, maximum, chromosome_size):
    
    return [random.randint(minimum, maximum) for _ in range(chromosome_size)]


def create_population(population_size, minimum,
                      maximum, chromosome_size):
    return [chromosome(minimum, maximum, chromosome_size)
            for _ in range(population_size)]


def fitness_fn(chromosome):
    
    checkmates = 0
    pairs = list(zip(chromosome,
                     [i+1 for i in range(len(chromosome))]))

    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            x, y = pairs[i]
            w, z = pairs[j]
            if x == w or y == z:
                checkmates += 1
            else:
                dx = abs(x - w)
                dy = abs(y - z)
                if dx == dy:
                    checkmates += 1
    fitness = max_atacking_pairs - checkmates
    return fitness

def select_parents(population, probabilities, qtd_parents=2):
        
    parents = []
    
    for _ in range(qtd_parents):
        draw = random.random()
        for (i, parent) in enumerate(population):
            if draw <= probabilities[i]:
                parents.append(parent)
                break
    return tuple(parents)

def reproduce(x, y):
    
    chromosome_size = len(x)
    point = random.randint(1, chromosome_size-1)
    return x[: point] + y[point :]


def mutate(chromosome):
    
    chromosome_size = len(chromosome)
    point = random.randint(0, chromosome_size - 1)
    new_value = random.randint(1, chromosome_size)
    
    while new_value == chromosome[point]:
        new_value = random.randint(1, chromosome_size)
    chromosome[point] = new_value
    return chromosome

def ga_eight_queens(population, fitness_fn, epochs=100):
    
    i = 0
    solutions = []
    
    while i < epochs:    
        new_population = []
        individual_fitness = [fitness_fn(chromosome) for chromosome in population]
        total_fitness = sum(individual_fitness)
        percentage_fitness = [fitness/total_fitness for fitness in individual_fitness]
        probabilities = [sum(percentage_fitness[:i+1]) for i in range(len(percentage_fitness))]

        if max_atacking_pairs in individual_fitness:
             
            break
        
        for _ in range(len(population)):
            x, y = select_parents(population, probabilities)
            child = reproduce(x, y)
            if random.random() <= mutation_probability:
                child = mutate(child)
            new_population.append(child)
        population = new_population
        i += 1
    return (argmax([fitness_fn(e) for e in population]), population)

board_size = 8
mutation_probability = 0.05
population_size = 1000
chromosome_size = board_size
minimum = 1
maximum = board_size
epochs = 100
max_atacking_pairs = int(comb(chromosome_size, 2))
population = create_population(population_size, minimum, maximum, chromosome_size)

index_best_individual, population = ga_eight_queens(population, fitness_fn, epochs)
solutions = list(
    filter(lambda individual: max_atacking_pairs == fitness_fn(individual),
           population))
print('solutions: ', solutions)

