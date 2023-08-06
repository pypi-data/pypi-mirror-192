const CommandType = require('../../utils/CommandType')
const LoadLibrary = require('./LoadLibraryHandler')
const GetType = require('./GetTypeHandler')
const InvokeStaticMethod = require('./InvokeStaticMethodHandler')
const GetStaticField = require('./GetStaticFieldHandler')
const SetStaticField = require('./SetStaticFieldHandler')
const ResolveReference = require('./ResolveReferenceHandler')
const CreateClassInstance = require('./CreateClassInstanceHandler')
const GetInstanceField = require('./GetInstanceFieldHandler')
const InvokeInstanceMethodHandler = require('./InvokeInstanceMethodHandler')
const DestructReference = require("./DestructReferenceHandler");
const Cast = require('./CastingHandler')
const InvokeGlobalMethod = require('./InvokeGlobalMethodHandler')

const ReferenceCache = require('./ReferencesCache')

function isResponseSimpleType(response) {
    let type = typeof(response)
    return ['string', 'boolean', 'number'].includes(type)
}

function isResponseArray(response) {
    return response instanceof Array
}

const handlers = {
    [CommandType.LoadLibrary]: LoadLibrary,
    [CommandType.InvokeStaticMethod]: InvokeStaticMethod,
    [CommandType.GetType]: GetType,
    [CommandType.GetStaticField]: GetStaticField,
    [CommandType.SetStaticField]: SetStaticField,
    [CommandType.CreateClassInstance]: CreateClassInstance,
    [CommandType.Reference]: ResolveReference,
    [CommandType.Cast]: Cast,
    [CommandType.GetInstanceField]: GetInstanceField,
    [CommandType.InvokeInstanceMethod]: InvokeInstanceMethodHandler,
    [CommandType.InvokeGlobalMethod]: InvokeGlobalMethod,
    [CommandType.DestructReference]: DestructReference
}

class Handler {
    handleCommand(command) {
        let result = handlers[command.commandId].handleCommand(command)
        if(isResponseSimpleType(result)) {
            return command.createResponse(result)
        } else if (isResponseArray(result)) {
            return command.createArrayResponse(result)
        } else {
            let cache = ReferenceCache.getInstance()
            let uuid = cache.cacheReference(result)
            return command.createReference(uuid)
        }
    }
}

module.exports.Handler = Handler
module.exports.handlers = handlers

