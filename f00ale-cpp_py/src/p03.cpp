#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p03(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    std::vector<std::string> v;

    {
        int num = 0;
        bool havenum = false;
        bool first = true;
        v.emplace_back("");
        for (const auto c: input) {
            if (c == '\n') {
                v.back() += '.';
                first = true;
            } else {
                if(first) {
                    v.emplace_back(".");
                    first = false;
                }
                v.back() += c;
            }
        }
        v.front() = std::string(v[1].size(), '.');
        v.emplace_back(v[1].size(), '.');
    }

    for(size_t row = 0; row < v.size(); row++) {
        for(size_t col = 0; col < v[row].size(); col++) {
            char c = v[row][col];
            if(c != '.' && !(c >= '0' && c <= '9')) {
                auto takenum = [&v](int r, int c) {
                    if(!(v[r][c] >= '0' && v[r][c] <= '9')) return 0;
                    while((v[r][c-1] >= '0' && v[r][c-1] <= '9')) c--;
                    int ret = 0;
                    while((v[r][c] >= '0' && v[r][c] <= '9')){
                        ret *= 10;
                        ret += v[r][c] - '0';
                        v[r][c] = '.';
                        c++;
                    }
                    return ret;
                };
                int a2tmp = 0;
                for(int dy = -1; dy <=1; dy++) {
                    for(int dx = -1; dx <=1; dx++) {
                        if(dx || dy) {
                            auto tmp = takenum(row+dy, col+dx);
                            ans1 += tmp;
                            if(c == '*' && tmp) {
                                if(a2tmp) ans2 += a2tmp*tmp;
                                else a2tmp = tmp;
                            }
                        }
                    }
                }
            }
        }
    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
