#!/usr/bin/env python3

import ast
import itertools
import operator
import re

operator_map = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Invert: operator.neg,
}

def get_number_input():
    print('Please input 4 single digit integers separated by spaces:')
    number_input = input()
    numbers_split = number_input.split(' ')

    number_regex = re.compile('^\d \d \d \d$')
    match_obj = number_regex.search(number_input)
    if (match_obj is None):
        raise ValueError('Unable to parse input as 4 single digit integers.')

    numbers_list = list(map(int, numbers_split))
    return numbers_list

def get_target_number_input():
    print('Input the target number:')
    target_input = input()

    number_regex = re.compile('^\-?\d+$')
    match_obj = number_regex.search(target_input)
    if (match_obj is None):
        raise ValueError('Please input a correct number.')

    target = int(target_input)
    return target

def get_number_permutations(numbers):
    return set(itertools.permutations(numbers))

def get_operator_permutations(operators, operator_count):
    return set(itertools.permutations(operators, operator_count))

def generate_calculation_expressions(elements):
    e1 = '(({n1} {o1} {n2}) {o2} {n3} ) {o3} {n4}'
    e2 = '({n1} {o1} {n2}) {o2} ({n3} {o3} {n4})'
    expressions = [e1, e2]
    for i in range(len(expressions)):
        e = expressions[i]
        e = e.format(n1 = elements[0], o1 = elements[1], n2 = elements[2], o2 = elements[3], n3 = elements[4], o3 = elements[5], n4 = elements[6])
        expressions[i] = e
    return expressions

def generate_calculation_elements(numbers, operators):
    elements = []
    count = len(numbers)
    for i in range(count):
        if (i != 0):
            operator = operators[i - 1]
            elements.append(operator)
        number = str(numbers[i])
        elements.append(number)
    return elements

def generate_calculation_expression(numbers, operators):
    count = len(numbers)
    expression = ''
    for i in range(count):
        if (i != 0):
            operator = operators[i - 1]
            expression += operator
        number = numbers[i]
        expression += str(number)
    return expression

def calculate(node):
    if (isinstance(node, ast.BinOp)):
        # When binary operation, recursively calculate left and right node
        left = calculate(node.left)
        right = calculate(node.right)
        operator = node.op
        return operator_map[type(operator)](left, right)

    elif (isinstance(node, ast.Num)):
        # When number, return number
        return node.n

def output_to_console(results):
    print('---------------')
    if (len(results) == 0):
        print('No expression found.')
    else:
        for r in results: print(r)
    print('---------------')

def execute():
    # Get user input
    try:
        numbers = get_number_input()
        target = get_target_number_input()
    except ValueError as e:
        print(e)
        return False

    # Get number permutations
    number_permutations = get_number_permutations(numbers)

    # Get operator permutations
    operators = '+-*/'
    operator_count = len(numbers) - 1
    operator_permutations = get_operator_permutations(operators, operator_count)

    # Try every permutation until target number is found
    correct_results = []
    for number_permutation in number_permutations:
        for operator_permutation in operator_permutations:
            elements = generate_calculation_elements(number_permutation, operator_permutation)
            expressions = generate_calculation_expressions(elements)
            for expression in expressions:
                # Parse expression
                module_tree = ast.parse(expression)
                expr_tree = module_tree.body[0].value

                try:
                    # Calculate result
                    result = calculate(expr_tree)
                except ZeroDivisionError:
                    # Skip when divided by zero
                    continue

                # Add expression to correct results when equal to target value
                if (result == target):
                    correct_results.append(expression)

    # Output correct results to console
    output_to_console(correct_results)
    return True

if (__name__ == '__main__'):
    end_loop = False
    while(end_loop is False):
        end_loop = execute()

