class Argument:
    def __init__(self, type, description, check=None):
        self.type = type
        self.description = description
        self.check = check

    def get_type(self):
        return self.type

    def get_description(self):
        return self.description

    def get_check(self):
        return self.check

    def __str__(self) -> str:
        args_str = "\t- Type: %s\n" % self.type
        args_str += "\t- Description: %s\n" % self.description
        if self.check:
            args_str += "\t- Check: %s\n" % str(self.check)
        return args_str


class ArgumentDirections:
    def __init__(self):
        self.inputs = {}
        self.outputs = {}

    def add_input(self, name, input):
        self.inputs[name] = input

    def add_output(self, name, output):
        self.outputs[name] = output

    def get_inputs(self):
        return self.inputs

    def get_outputs(self):
        return self.outputs

    def __str__(self) -> str:
        args_str = ""
        for k, v in self.inputs.items():
            args_str += "- Input: %s\n" % k
            args_str += "%s" % v
        for k, v in self.outputs.items():
            args_str += "- Output: %s\n" % k
            args_str += "%s" % v
        return args_str
