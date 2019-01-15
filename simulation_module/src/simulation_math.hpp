#pragma once

#include <vector>

#include <functional>

template <typename T>
class Matrix {
public:
    explicit Matrix(unsigned int x, unsigned int y) 
        : sizeX(x), sizeY(y) {
        data.resize(sizeX * sizeY); //Resize our vector to accomodate our data
    }

    T& operator()(unsigned int x, unsigned int y) {
        if(x < 0 || y < 0 || x >= sizeX || y >= sizeY)
            throw std::out_of_range("OOB Access!");
        return data[sizeX*y + x];
    }

    T& operator[](unsigned int idx) {
        if(idx < 0 || idx >= data.size())
            throw std::out_of_range("OOB Access!");
        return data[idx];
    }

    void Populate(std::function<void(const std::vector<T>)> functor) {
        functor(data);
    }
private:
    std::vector<T> data;
    unsigned int sizeX, sizeY;

};