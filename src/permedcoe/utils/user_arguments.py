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
        args_str = f"\t- Type: {self.type}\n"
        args_str += f"\t- Description: {self.description}\n"
        if self.check:
            args_str += f"\t- Check: {self.check}\n"
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
            args_str += f"- Input: {k}\n"
            args_str += f"{v}"
        for k, v in self.outputs.items():
            args_str += f"- Output: {k}\n"
            args_str += f"{v}"
        return args_str


class Arguments:
    def __init__(self):
        self.arguments = {}
        self.arguments["default"] = ArgumentDirections()
        self.description = "Undefined description."

    def set_description(self, description):
        self.description = description

    def add_input(self, name, type, description, check=None, mode="default"):
        if not mode in self.arguments:
            self.arguments[mode] = ArgumentDirections()
        self.arguments[mode].add_input(name, Argument(type, description, check))

    def add_output(self, name, type, description, mode="default"):
        if not mode in self.arguments:
            self.arguments[mode] = ArgumentDirections()
        self.arguments[mode].add_output(name, Argument(type, description))

    def get_arguments(self) -> dict:
        return self.arguments

    def get_description(self):
        return self.description

    def __str__(self) -> str:
        args_str = ""
        for k, v in self.arguments.items():
            args_str += f"Mode: {k}\n"
            args_str += f"Arguments: {v}\n"
        return args_str
