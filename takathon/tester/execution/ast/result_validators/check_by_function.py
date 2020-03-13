from dataclasses import dataclass

from takathon.tester.execution.ast.result_validators.call_function import CallFun


@dataclass
class CheckByFunction(CallFun):
    validator_function : str

    def execute(self, local_scope):
        result = self.call_fun(local_scope)
        validator = eval(self.validator_function,
                         self.module.__dict__, local_scope)

        try:
            assert validator(result)
            self.test_results.passed += 1
        except AssertionError:
            self.test_results.errors += 1
            print(f'Error in function {self.fname} arguments {self.args}: '
                  f'Function {self.validator_function} rejected result {result}')
