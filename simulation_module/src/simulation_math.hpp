#pragma once

#include <vector>
#include <random>
#include <functional>

template <typename T>
class Matrix
{
  public:
    explicit Matrix(unsigned int x, unsigned int y)
        : sizeX(x), sizeY(y)
    {
        data.resize(sizeX * sizeY); //Resize our vector to accomodate our data
    }

    T &operator()(unsigned int x, unsigned int y)
    {
        if (x < 0 || y < 0 || x >= sizeX || y >= sizeY)
            throw std::out_of_range("OOB Access!");
        return data[sizeX * y + x];
    }

    T &operator[](unsigned int idx)
    {
        if (idx < 0 || idx >= data.size())
            throw std::out_of_range("OOB Access!");
        return data[idx];
    }

    void Populate(std::function<void(const std::vector<T>)> functor)
    {
        functor(data);
    }

  private:
    std::vector<T> data;
    unsigned int sizeX, sizeY;
};

template <typename T>
std::vector<T> space(T maxvalue, T step)
{
    auto ret = std::vector<T>(maxvalue / step);
    auto n = 0UL;
    for (auto i = 0UL; i < maxvalue / step; i++)
    {
        ret[i] = n;
        n += step;
    }

    return ret;
}

class ProbabilityDensityFunction
{
  public:
    explicit ProbabilityDensityFunction(std::vector<double> pdf, std::vector<double> values, size_t binSize) : values_(values), binSize_(binSize)
    {
        distribution_ = std::discrete_distribution<int>(pdf.begin(), pdf.end());
    }
    ProbabilityDensityFunction(std::vector<double> pdf)
    {
        distribution_ = std::discrete_distribution<int>(pdf.begin(), pdf.end());
        values_ = space<double>(pdf.size(), 1.0);
    }
    ProbabilityDensityFunction()
    {
        values_ = std::vector<double>();
        binSize_ = 0;
    }

    double SampleValue()
    {
        auto value = distribution_(generator);
        return values_[value];
    }

  private:
    std::default_random_engine generator;
    std::discrete_distribution<int> distribution_;
    std::vector<double> values_;
    size_t binSize_;
};
