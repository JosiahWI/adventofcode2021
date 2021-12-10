#!/usr/bin/env python3

import pathlib

class SyntaxChecker:

    bad_token_score = {
        ")" : 3,
        "]" : 57,
        "}" : 1197,
        ">" : 25137 
    }

    fix_token_score = {
        "(" : 1,
        "[" : 2,
        "{" : 3,
        "<" : 4
    }

    token_pair = {
        "(" : ")",
        "[" : "]",
        "{" : "}",
        "<" : ">"
    }

    def __init__(self):
        self._token_stack = []

    def check_expression(self, exp):
        """Check that an expression is not corrupt."""
        if self._token_stack != []:
            raise RuntimeError("Stack must be reset.")
        for token in exp:
            if token in self.token_pair:
                self._token_stack.append(token)
            elif self._token_stack != []:
                # the last item on the stack is always an opening token
                if self.token_pair[self._token_stack[-1]] == token:
                    self._token_stack.pop(-1)
                else:
                    raise CorruptSyntaxError(self.bad_token_score[token])

        if self._token_stack != []:
            raise IncompleteSyntaxError()

    def repair_stack(self):
        # We cheat a bit here. We don't actually bother to modify
        # the stack. We just count the score and reset it.
        score = 0
        for token in self._token_stack[::-1]:
            score *= 5
            score += self.fix_token_score[token]
        self.reset_stack()
        return score

    def reset_stack(self):
        """Clear the stack of left over tokens so we can use it again."""
        self._token_stack = []

class CorruptSyntaxError(SyntaxError):

    def __init__(self, score, *args, **kwargs):
        self.score = score
        super().__init__(*args, **kwargs)

class IncompleteSyntaxError(SyntaxError):
    pass

if __name__ == "__main__":
    with open(pathlib.Path(__file__).parent / "input.txt", "r") as fp:
        exprs = [line.strip() for line in fp]

    checker = SyntaxChecker()
    corrupt_score_sum = 0
    incomplete_score_sums = []
    for exp in exprs:
        try:
            checker.check_expression(exp)
        except CorruptSyntaxError as e:
            corrupt_score_sum += e.score
            checker.reset_stack()
        except IncompleteSyntaxError as e:
            incomplete_score_sums.append(checker.repair_stack())
            
    print(f"Part 1: {corrupt_score_sum}")
    ordered_sums = sorted(incomplete_score_sums)
    print(f"Part 2: {ordered_sums[(len(ordered_sums) - 1) // 2]}")
