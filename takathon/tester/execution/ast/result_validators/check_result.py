from dataclasses import dataclass

from takathon.tester.execution.ast.result_validators.call_function import CallFun


@dataclass
class CheckResult(CallFun):
    expected_result : str

    def execute(self, local_scope):
        result = self.call_fun(local_scope)
        expected_result = eval(self.expected_result,
                               self.module.__dict__, local_scope)

        try:
            assert result == expected_result
            self.test_results.passed += 1
        except AssertionError:
            self.test_results.errors += 1
            print(f'Error in function {self.fname} arguments {self.args}:'
                  f'Expected {expected_result} got {result}')
