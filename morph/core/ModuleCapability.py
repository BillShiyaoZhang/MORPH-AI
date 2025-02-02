class ModuleCapability:
    def __init__(self, capability_name: str, description: str):
        self.capability_name = capability_name
        self.description = description

    def execute(self, *args, **kwargs):
        raise NotImplementedError()

    def get_input_description(self):
        raise NotImplementedError()

    def get_input_examples(self):
        raise NotImplementedError()

    def get_output_schema(self):
        raise NotImplementedError()

    def get_output_description(self):
        raise NotImplementedError()
 
    def get_output_examples(self):
        raise NotImplementedError()

    def get_input_schema(self):
        raise NotImplementedError()

    def varify(self):
        raise NotImplementedError()