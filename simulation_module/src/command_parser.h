#pragma once
#include <napi.h>

class CommandParser
{
public:
    explicit CommandParser();
    void ExecuteCommand();

private:
    int m_NumCommands;
};