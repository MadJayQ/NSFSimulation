#pragma once

#include "simulation_math.hpp"


class BudgetMatrix : Matrix<float>
{
public:
    explicit BudgetMatrix(unsigned int x, unsigned int y);
}