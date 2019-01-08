#include "command_parser.h"

#include <iostream>

/*
CommandParser::CommandParser(const Napi::CallbackInfo& info) : ObjectWrap(info) {

}

Napi::Function CommandParser::GetClass(Napi::Env env) {
    return DefineClass(env, "CommandParser", {});
}

void CommandParser::Init(Napi::Env& env, Napi::Object& exports) {
    Napi::String name = Napi::String::New(env, "CommandParser");
    exports.Set(name, CommandParser::GetClass(env));
}
*/

CommandParser::CommandParser() :
    m_NumCommands(0)
{

}


void CommandParser::ExecuteCommand()
{
    std::cout << "There have been" << (m_NumCommands++) << " commands executed!" << std::endl;
}