#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>
#include <cmath>

std::tuple<std::string, std::string> p04(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    std::vector<std::vector<int>> winning;
    {
        int num = 0;
        bool havenum = false;
        bool pipe = 0;
        int ant = 0;
        std::vector<int> v1, v2;
        int card = 0;
        int ncards = 1;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else {
                if(havenum) {
                    ant++;
                    if(ant > 1) {
                        if(pipe) {
                            v2.push_back(num);
                        } else {
                            v1.push_back(num);
                        }
                    }
                }
                if(c == '|') pipe= true;
                if(c=='\n') {
                    std::sort(v1.begin(), v1.end());
                    std::sort(v2.begin(), v2.end());
                    std::vector<int> out;
                    std::set_intersection(v1.begin(), v1.end(), v2.begin(), v2.end(), std::back_inserter(out));
                    if(out.size()) {
                        ans1 += std::pow(2, out.size()-1);
                    }
                    if(pipe) winning.emplace_back(std::move(out));
                    pipe = false;
                    ant = 0;
                    v1.clear();
                    v2.clear();
                    card++;
                }
                havenum = false;
                num = 0;
            }
        }

        std::vector<int> copies(winning.size(), 1);
        for(int i = 0; i < winning.size(); i++) {
            int c = copies[i];
            for(int j = 0; j < winning[i].size(); j++) {
                copies[i+1+j] += c;
            }
        }
        for(auto c : copies) ans2 += c;

    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
