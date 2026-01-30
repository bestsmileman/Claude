#!/usr/bin/env python3
"""
Arithmetic Expression Evaluator

Supports: +, -, *, /, parentheses, unary minus, integer and float literals.
Uses a recursive descent parser for correct operator precedence.

Grammar:
    expr   -> term (('+' | '-') term)*
    term   -> factor (('*' | '/') factor)*
    factor -> ('+' | '-') factor | atom
    atom   -> NUMBER | '(' expr ')'
"""

import sys


class ParseError(Exception):
    pass


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.tokens = []
        self._tokenize()
        self.idx = 0

    def _tokenize(self):
        i = 0
        while i < len(self.text):
            ch = self.text[i]
            if ch.isspace():
                i += 1
                continue
            if ch in "+-*/()":
                self.tokens.append(ch)
                i += 1
            elif ch.isdigit() or ch == ".":
                start = i
                has_dot = ch == "."
                i += 1
                while i < len(self.text) and (self.text[i].isdigit() or (self.text[i] == "." and not has_dot)):
                    if self.text[i] == ".":
                        has_dot = True
                    i += 1
                self.tokens.append(self.text[start:i])
            else:
                raise ParseError(f"Unexpected character: '{ch}' at position {i}")

    def peek(self):
        if self.idx < len(self.tokens):
            return self.tokens[self.idx]
        return None

    def advance(self):
        tok = self.peek()
        self.idx += 1
        return tok

    def expect(self, expected):
        tok = self.advance()
        if tok != expected:
            raise ParseError(f"Expected '{expected}', got '{tok}'")
        return tok


class Parser:
    def __init__(self, tokenizer):
        self.tok = tokenizer

    def parse(self):
        result = self._expr()
        if self.tok.peek() is not None:
            raise ParseError(f"Unexpected token: '{self.tok.peek()}'")
        return result

    def _expr(self):
        left = self._term()
        while self.tok.peek() in ("+", "-"):
            op = self.tok.advance()
            right = self._term()
            if op == "+":
                left = left + right
            else:
                left = left - right
        return left

    def _term(self):
        left = self._factor()
        while self.tok.peek() in ("*", "/"):
            op = self.tok.advance()
            right = self._factor()
            if op == "*":
                left = left * right
            else:
                if right == 0:
                    raise ParseError("Division by zero")
                left = left / right
        return left

    def _factor(self):
        if self.tok.peek() == "+":
            self.tok.advance()
            return self._factor()
        if self.tok.peek() == "-":
            self.tok.advance()
            return -self._factor()
        return self._atom()

    def _atom(self):
        tok = self.tok.peek()
        if tok is None:
            raise ParseError("Unexpected end of expression")
        if tok == "(":
            self.tok.advance()
            result = self._expr()
            self.tok.expect(")")
            return result
        # Must be a number
        self.tok.advance()
        try:
            if "." in tok:
                return float(tok)
            return int(tok)
        except ValueError:
            raise ParseError(f"Invalid number: '{tok}'")


def evaluate(expression):
    """Evaluate an arithmetic expression string and return the result."""
    tokenizer = Tokenizer(expression)
    parser = Parser(tokenizer)
    return parser.parse()


def format_result(value):
    """Format the result: show as int if it's a whole number, else as float."""
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


def main():
    if len(sys.argv) > 1:
        expression = " ".join(sys.argv[1:])
    else:
        expression = input().strip()

    if not expression:
        print("Error: empty expression")
        sys.exit(1)

    try:
        result = evaluate(expression)
        print(format_result(result))
    except ParseError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
