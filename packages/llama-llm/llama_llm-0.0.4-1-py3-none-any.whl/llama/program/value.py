from llama.program.util.run_ai import query_run_program

class Value:
    def __init__(self, type, data=None):
        self.type = type
        self.data = data
        self.function = None
        self.index = None

    def get_field(self, name):
        if self.data is None:
            self._compute_value()

        return self.data._get_attribute_raw(name)

    def set_function(self, function):
        self.function = program

    def __str__(self):
        if self.data is None:
            self._compute_value()

        return str(self.data)

    def _compute_value(self):
        params = {
            "program": self.function.program.to_dict(),
            "requested_value": self.index,
        }
        
        response = query_run_program(params)

        response.raise_for_status()
        self.data = self.type.parse_obj(response.json()["data"])




