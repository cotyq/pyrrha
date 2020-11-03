class Report:
    def __init__(self):
        self.results = {}

    def add_result(self, function_name, result):
        self.results[function_name] = result

    def compare(self, report):
        pass
