from javonet.core.handler.HandlerDictionary import handler_dict
from javonet.sdk.core.PythonCommand import PythonCommand


class AbstractCommandHandler:
    pass
    _required_parameters_count = 0

    def HandleCommand(self, python_command):
        try:
            self.iterate(python_command)
            return self.process(python_command)
        except Exception as e:
            raise e

    def iterate(self, command):
        for i in range(0, len(command.payload)):
            if isinstance(command.payload[i], PythonCommand):
                try:
                    command.payload[i] = handler_dict.get(command.payload[i].command_type).HandleCommand(command.payload[i])
                except Exception as e:
                    raise e

    def process(self, python_command):
        pass
