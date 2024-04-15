import inspect

class Test():
  
    def a(self):
        pass
    def b(self):
        pass

test_instance = Test()

print(len(inspect.getmembers(Test, inspect.isfunction)))
