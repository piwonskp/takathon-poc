# Takathon - Proof of Concept
Takathon is a language focused on QA and unit testing.

# Design Goals
The main goal is similiar to [Specification by example](https://en.wikipedia.org/wiki/Specification_by_example) goals, namely to merge tests, documentation and type system into one thing called specification. Specification describes a chunk of code (e.g. function).

This approach has plenty of benefits:
* Declarative and readable tests
* Documentation and usage examples generated directly from specification
* Helpful error messages
* Easier debugging
* Testing in real time
* Native TDD support

# Usage
Testing factorial function for several arguments and expected exception:
```
test factorial(n):
     domain -1:
            throws ValueError('factorial() not defined for negative values')
     domain 0: results 1
     domain 1: results 1
     domain 3: results 6
     domain 4: results 24
     domain 5: results 120
def:
    if n < 0:
       raise ValueError('factorial() not defined for negative values')

    if n == 0:
        return 1
    return n * factorial(n-1)
```
Other examples are located in [examples/](examples) directory. To test a specific file you can use `takathon test <file-name>` command inside docker container

# Relation to Python
Factorial example compiles to following Python code when executing:
```
def factorial(n):
    if n < 0:
       raise ValueError('factorial() not defined for negative values')

    if n == 0:
        return 1
    return n * factorial(n-1)
```
The language is purely development oriented and adds no complexity to the runtime.
# Development
Preferred way is to use docker for development. To run the tool install docker-compose and type `docker-compose run --rm app`.
