# Regular Expression Derivative Evaluator

## Overview

The goal of this assignment is to implement a regular expression
evaluator by the derivative method. The evaluator will take a regular expression in the form of regular expression classes defined in the `regex.py` module, and a string to match as input. it will provide pattern matching against the input
string, producing the result of the matching operation by returning
*true* if the match succeeds and *false* otherwise. 

You should re-read the material on regular expression derivatives
before you begin this assignment. Use that material as a reference.

## Setup

First, you need to download the project from github. The files included are:
`regexp.py`, `testregex.py`, and the usual script `submit.py`.

You will do all of your code development in `regexp.py`. Use `testregex.py` to run tests of your code as you develop it. You may also use the `main` function to test as well. Run the test module with:
`python -m pytest -v testregex.py`. Note that we have provided a few tests for you, and suggested at others for you to implement. We will be running your code on at least the tests included in the test file. Make up any tests you deem inmportant. Remember: testing should be more than 50% of your development time!

### Regular Expression Classes

A regular expression is represented by the following classes:

1. NullSet: The NULL regex
2. Epsilon: The empty regex
3. Character('char'): A regex of one symbol
4. Sequence(re1, re2): Conatenation of two regexs
5. Alternation(re1, re2): Union (OR) of two regexs
6. Closure(re): Zero to any number of of a regex

The constructors of each class are shown above. The first two classes do not have constructors. The term "re" denotes an instance of one of the regex classes. Thus, the `Character` class has a character member variable, the `Sequence` and `Alternation` classes have two regular expression objects as members, and `Closure` has a single regular expression object as a member. 

In addition to the constructors mentioned above, each regex must implement a protocol that allows it to participate in the derivative matching proceedure. 

Here is a summary of the methods each regex class must implement:

**delta:**: The `delta` method takes no parameters and returns a regex class. It implements the &delta; function
defined in the course material and below. This function is a test if the regex can match the empty regex, `Epsilon`. That is, it returns the "empty" regular
expression `Epsilon` if the regular expression (self) matches "empty", it returns the null regex `NullSet` otherwise. Recall that the
empty regular expression &epsilon; matches the empty string and &empty;
matches nothing.

The following lists the rules for the delta method. The order corresponds toi the class order in the list above.

* **E1:** &delta;(&empty;) = &empty;
* **E2:** &delta;(&epsilon;) = &epsilon;
* **E3:** &delta;(c) = &empty;
* **E4:** &delta;(re<sub>1</sub> re<sub>2</sub>) =
  &delta;(re<sub>1</sub>) &delta;(re<sub>2</sub>)
* **E5:** &delta;(re<sub>1</sub>|re<sub>2</sub>) =
  &delta;(re<sub>1</sub>) | &delta;(re<sub>2</sub>)
* **E5:** &delta;(re*) = &epsilon;

**is_empty:**: This method takes no argument and returns `True` if a regex matches empty
(in the atomic sense), or `False` otherwise. The only regular expressions that return `True` are `Epsilon` and `Closure`. All the rest just return `False`. This method is called after delta at the end of matching to determine success or failure of the match.

**derive(char):**: This method takes a single character literal as an argument and returns a regular expression class. It implements the rule for
regular expression derivatives. You will need to
implement the derivative rule for each of the classes above. The `derive` method
yields a new regular expression object with respect to the
character argument `char`. Note, the derivative rules are exactly that -
they describe rules that *generate a new regular expression* based off
of the current regular expression and some character `char`. The numbers correspond to the class list above. Note two rules apply to `Character`. The | character mean an alternation.

* **D1:** D<sub>c</sub>(&empty;) = &empty;
* **D2:** D<sub>c</sub>(&epsilon;) = &empty;
* **D3:** D<sub>c</sub>(c) = &epsilon;
* **D3:** D<sub>c</sub>(c&prime;) = &empty; if c &ne; c&prime;
* **D4:** D<sub>c</sub>(re<sub>1</sub> re<sub>2</sub>) =
    &delta;(re<sub>1</sub>)D<sub>c</sub>(re<sub>2</sub>) |
    D<sub>c</sub>(re<sub>1</sub>)re<sub>2</sub>
* **D5:** D<sub>c</sub>(re<sub>1</sub> | re<sub>2</sub>) =
  D<sub>c</sub>(re<sub>1</sub>) | D<sub>c</sub>(re<sub>2</sub>)
* **D6:** D<sub>c</sub>(re\*) = D<sub>c</sub>(re) re\*;

**normalize:**: This method takes no argument and returns a regular expression object. It implements the "evaluation" of a
regular expression after taking its derivative. This method implements
the implicit nature of the theoretical aspect of regular expression
derivatives. After you apply the derivative, the next step is to 
*normalize* its form with respect to the application of `delta` and
the `derivative`. Here are the rules you need to consider during
normalization (we use N to indicate a call to `normalize`). Note that rules 4-8 apply to `Sequence`, rules 9-11 apply to `Alternation`.

1. N(&epsilon;) = &epsilon;
1. N(&empty;) = &empty;
1. N(c) = c
1. N(&empty; re<sub>2</sub>) = &empty;
1. N(re<sub>1</sub> &empty;) = &empty;
1. N(re<sub>1</sub> &epsilon;) = N(re<sub>1</sub>)
1. N(&epsilon; re<sub>2</sub>) = N(re<sub>2</sub>)
1. N(re<sub>1</sub> re<sub>2</sub>) = N(re<sub>1</sub>) N(re<sub>2</sub>)
1. N(re<sub>1</sub>|&empty;) = N(re<sub>1</sub>)
1. N(&empty;|re<sub>2</sub>) = N(re<sub>2</sub>)
1. N(re<sub>1</sub>|re<sub>2</sub>) = N(re<sub>1</sub>)|N(re<sub>2</sub>)
1. N(re\*) = N(re)\*

In addition to the classes specified above, you will implement two functions in the `regexp.py` module. the first method is the high-level function that carries out the matching process according to these rules:

## Matching Rules

* **R1:** If string to match is empty and the current pattern matches empty, then the match succeeds. The test calls delta and then is_empty on the regex object to determine if the regex matches empty.
* **R2:** If the string to match is non-empty, the new pattern is the derivative of the current pattern with respect to the first character of the current string, and the new string to match is the remainder of the current string.

**matches(regex, string):**: This method takes a regular expression class instance and the string of characters to be matched as arguments. It returns `True` if the string matches the pattern represented by the regex, `False` otherwise.  

It processes the string one character at a time. At each character it takes the derivative of the regex with respect to the character. That is, it class the derive function on the regex object, then calls normalize on the regex object returned by derive (not necessarily the same object). If the result of derive and normalize is the null set we can return `False`. Otherwise, call `matches` on the rest of the string. If the sting is empty, we call delta and then is_empty on the regex object and return that result (rule **R1**).

The other function in the `regexp.py` module you will write is: 

**make_str(string):**: This method takes a string argument and returns a regex `Sequence` object. This method provides a convenient way of producing a regular expression that consists of a concatenation of more than two symbols (characters). The way you build a string is by recursion, where each `Sequence` contains a `Character`, `Sequence` pair. The end of the chain is the `Sequence` that consists of the pair: `Character, `Epsilon`.

For example, the string 'abc' would be represented as:

Sequence(Character('a'),
                  Sequence(Character('b'),
                                  Sequence(Character('c'), Epsilon())))

## Development Notes:

The best way to approach any project is to work incrementally. So,
first create the regular expression classes and implement each of the methods using `pass` in the body.

Focus on the first three classes at the beginning and build from there.

Don't worry about the `make_str` function. Write `matches` and the first three classes. Run tests on those with simple input.

**Note:** it might be best to implement each method one-by-one and
test them to make sure they are working properly. You
may want to add some debugging methods or use the debugger.

## Additional Notes

**is_empty:**: This method is simple. You should simply return
a boolean for each regular expression that indicates if it is "empty" or
"null".

**delta:**: Most of the implementations are extremely
simple. The implementation for sequences and alternative require some
additional work to determine if they are "empty" or "null".

**derivative('char'):**: Remember, all you are doing in this
method is creating a new regular expression that represents the
derivative of the regular expression you are invoking the `derivative`
method on. Again, the most complicated of these is the `Sequence` regular expression.

**normalize:**: If you follow the rules outlined above for
normalization you should not have too much trouble with this
method. This method is simplifying the regular expression based on the
result of taking the regular expression's derivative. Again, start
with the simple rules first, add some debugging support.

**Notes:** You should test your code step-by-step to ensure that it is
working properly. Do not write all of this at once and then test - it
will be too confusing and harder to debug. You should implement the
simple regular expressions first and then run tests to see if
it works on the simple cases. 

Continue in this fashion implementing and testing your code along the
way. In the end, you should run the tests and verify that all of
the provided tests pass- and any of your own making.

## Task 4: Submit Your Work

Submit only the `regexp.py` file for this assignment. use the `submit.py` script as usual.

