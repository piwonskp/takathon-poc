from dataclasses import dataclass

from takathon.tester.execution.ast.result_validators.call_function import CallFun


@dataclass
class CheckThrow(CallFun):
    expected_exc : str

    def execute(self, local_scope):
        try:
            self.call_fun(local_scope)
        except Exception as e:
            expected = eval(self.expected_exc, self.module.__dict__, local_scope)
            if type(expected) == type:
                expected = expected()

            try:
                assert (type(e) is type(expected)
                        and e.args == expected.args)

                self.test_results.passed += 1
            except AssertionError:
                self.test_results.errors +=1
                print(f'Wrong exception in function {self.fname} arguments {self.args}:'
                      f'Expected {type(expected)} got {type(e)}')
        else:
            self.test_results.errors +=1
            print(f'Error in function {self.fname} arguments {self.args}:'
                  f'Expected exception {self.expected_exc}. No exception has been raised')
