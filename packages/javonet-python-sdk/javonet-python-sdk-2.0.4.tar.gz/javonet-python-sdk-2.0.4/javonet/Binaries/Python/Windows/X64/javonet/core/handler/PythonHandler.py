import traceback

from javonet.core.handler.AbstractHandler import AbstractHandler
from javonet.core.handler.CommandHandler.CastingHandler import CastingHandler
from javonet.core.handler.CommandHandler.CreateClassInstanceHandler import CreateClassInstanceHandler
from javonet.core.handler.CommandHandler.DestructReferenceHandler import DestructReferenceHandler
from javonet.core.handler.CommandHandler.GetInstanceFieldHandler import GetInstanceFieldHandler
from javonet.core.handler.CommandHandler.GetStaticFieldHandler import GetStaticFieldHandler
from javonet.core.handler.CommandHandler.GetTypeHandler import GetTypeHandler
from javonet.core.handler.CommandHandler.InvokeInstanceMethodHandler import InvokeInstanceMethodHandler
from javonet.core.handler.CommandHandler.InvokeStaticMethodHandler import InvokeStaticMethodHandler
from javonet.core.handler.CommandHandler.LoadLibraryHandler import LoadLibraryHandler
from javonet.core.handler.CommandHandler.ResolveInstanceHandler import ResolveInstanceHandler
from javonet.core.handler.CommandHandler.SetStaticFieldHandler import SetStaticFieldHandler
from javonet.core.handler.HandlerDictionary import handler_dict
from javonet.core.handler.ReferencesCache import ReferencesCache
from javonet.core.handler.utils.ExceptionSerializer import ExceptionSerializer
from javonet.sdk.core.PythonCommandType import PythonCommandType


class PythonHandler(AbstractHandler):

    def __init__(self):
        load_library_handler = LoadLibraryHandler()
        invoke_static_method_handler = InvokeStaticMethodHandler()
        set_static_field_handler = SetStaticFieldHandler()
        create_class_instance_handler = CreateClassInstanceHandler()
        get_static_field_handler = GetStaticFieldHandler()
        resolve_instance_handler = ResolveInstanceHandler()
        get_type_handler = GetTypeHandler()
        invoke_instance_method_handler = InvokeInstanceMethodHandler()
        casting_handler = CastingHandler()
        get_instance_field_handler = GetInstanceFieldHandler()
        destruct_reference_handler = DestructReferenceHandler()

        handler_dict[PythonCommandType.LoadLibrary] = load_library_handler
        handler_dict[PythonCommandType.InvokeStaticMethod] = invoke_static_method_handler
        handler_dict[PythonCommandType.SetStaticField] = set_static_field_handler
        handler_dict[PythonCommandType.CreateClassInstance] = create_class_instance_handler
        handler_dict[PythonCommandType.GetStaticField] = get_static_field_handler
        handler_dict[PythonCommandType.Reference] = resolve_instance_handler
        handler_dict[PythonCommandType.GetType] = get_type_handler
        handler_dict[PythonCommandType.InvokeInstanceMethod] = invoke_instance_method_handler
        handler_dict[PythonCommandType.Cast] = casting_handler
        handler_dict[PythonCommandType.GetInstanceField] = get_instance_field_handler
        handler_dict[PythonCommandType.DestructReference] = destruct_reference_handler

    def HandleCommand(self, python_command):
        try:
            response = handler_dict.get(python_command.command_type).HandleCommand(python_command)
        except Exception as e:
            stack_trace = traceback.extract_stack()
            return ExceptionSerializer.serialize_exception(e, python_command, stack_trace)

        if self.__is_response_simple_type(response):
            return python_command.create_response(response)
        elif self.__is_response_array(response):
            return python_command.create_array_response(response)
        else:
            reference_cache = ReferencesCache()
            guid = reference_cache.cache_reference(response)
            return python_command.create_reference(guid)

    def __is_response_simple_type(self, response):
        return isinstance(response, (int, float, bool, str))

    def __is_response_array(self, response):
        return isinstance(response, list);
