# package calculator
import collections
from math import nan
from enum import Enum

# A calculator for rather simple arithmetic expressions.
# Your task is to implement the missing functions so the
# expressions evaluate correctly. Your program should be
# able to correctly handle precedence (including parentheses)
# and associativity - see helper functions.
# The easiest way to evaluate infix expressions is to transform
# them into postfix expressions, using a stack structure.
# For example, the expression 2*(3+4)^5 is first transformed
# to [ 3 -> 4 -> + -> 5 -> ^ -> 2 -> * ] and then evaluated
# left to right. This is known as Reverse Polish Notation,
# see: https://en.wikipedia.org/wiki/Reverse_Polish_notation
#
# NOTE:
# - You do not need to implement negative numbers
#
# To run the program, run either CalculatorREPL or CalculatorGUI

MISSING_OPERAND:  str = "Missing or bad operand"
DIV_BY_ZERO:      str = "Division with 0"
MISSING_OPERATOR: str = "Missing operator or parenthesis"
OP_NOT_FOUND:     str = "Operator not found"
OPERATORS:        str = "+-*/^"


def infix_to_postfix(tokens):
    # check_input(tokens)
    output = []
    operators = collections.deque()

    for char in tokens:
        if check_float(char):
            output.append(char)
        elif char in OPERATORS:
            if len(operators) != 0:
                top_of_stack = peek_at_deque(operators)

                if top_of_stack != '(':
                    precedence = compare_precedence(char, top_of_stack)
                    left_associativity = get_associativity(char) == Assoc.LEFT

                    while precedence == CompareValue.GREATER or precedence == CompareValue.EQUAL and left_associativity:
                        output.append(operators.pop())

                        if len(operators) != 0:
                            top_of_stack = peek_at_deque(operators)
                            precedence = compare_precedence(char, top_of_stack)
                            left_associativity = get_associativity(char) == Assoc.LEFT
                        else:
                            break

            operators.append(char)

        elif char == "(":
            operators.append(char)

        elif char == ")":
            top_of_stack = peek_at_deque(operators)

            while top_of_stack != "(":
                if len(operators) != 0:
                    output.append(operators.pop())
                else:
                    raise Exception(MISSING_OPERATOR)

                top_of_stack = peek_at_deque(operators)

            if top_of_stack == "(":
                operators.pop()

        else:
            raise Exception(MISSING_OPERAND)

    while len(operators) != 0:
        top_of_stack = peek_at_deque(operators)

        if top_of_stack != '(':
            output.append(operators.pop())
        else:
            raise Exception(MISSING_OPERATOR)

    return output


# -----  Evaluate RPN expression -------------------
def eval_postfix(postfix_tokens):
    operand_stack = collections.deque()

    for token in postfix_tokens:
        if check_float(token):
            operand_stack.append(float(token))
        if token in OPERATORS:
            d1 = operand_stack.pop()
            d2 = operand_stack.pop()
            result = apply_operator(token, d1, d2)
            if result is nan:
                raise Exception(DIV_BY_ZERO)
            else:
                operand_stack.append(result)

    return operand_stack[0]


# Method used in REPL
def eval_expr(expr: str):
    if len(expr) == 0:
        return nan
    tokens = tokenize(expr)
    postfix_tokens = infix_to_postfix(tokens)
    return eval_postfix(postfix_tokens)


def apply_operator(op: str, d1: float, d2: float):
    op_switcher = {
        "+": d1 + d2,
        "-": d2 - d1,
        "*": d1 * d2,
        "/": nan if d1 == 0 else d2 / d1,
        "^": d2 ** d1
    }
    return op_switcher.get(op, ValueError(OP_NOT_FOUND))


def get_precedence(op: str):
    op_switcher = {
        "+": 2,
        "-": 2,
        "*": 3,
        "/": 3,
        "^": 4
    }
    return op_switcher.get(op, ValueError(OP_NOT_FOUND))


class Assoc(Enum):
    LEFT = 1
    RIGHT = 2


def get_associativity(op: str):
    if op in "+-*/":
        return Assoc.LEFT
    elif op in "^":
        return Assoc.RIGHT
    else:
        return ValueError(OP_NOT_FOUND)


# ---------- Tokenize -----------------------
def tokenize(expr: str):
    temp_string = ''
    tokens = []

    for char in expr:
        if check_float(char) or char == ".":
            temp_string += char
        elif char in '()+-*/^':
            if len(temp_string) != 0:
                tokens.append(temp_string)
            tokens.append(char)
            temp_string = ''
        else:
            raise Exception(MISSING_OPERAND)
    if len(temp_string) != 0:
        tokens.append(temp_string)

    return tokens

# TODO Possibly more methods


class CompareValue(Enum):
    GREATER = 1
    EQUAL = 2
    LESS = 3


def compare_precedence(o1, o2):
    if get_precedence(o1) < get_precedence(o2):
        return CompareValue.GREATER
    if get_precedence(o1) == get_precedence(o2):
        return CompareValue.EQUAL
    else:
        return CompareValue.LESS


def check_input(test_input):  # TODO
    for i in range(len(test_input)):
        if (i + 1) % 2 == 0 and test_input[i] not in "+-*/^()":
            raise Exception(OP_NOT_FOUND)


def peek_at_deque(stack):
    top_of_stack = stack.pop()
    stack.append(top_of_stack)

    return top_of_stack


def check_float(potential_float):
    try:
        float(potential_float)

        return True
    except ValueError:
        return False

