#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p01(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    {
        static const std::vector<std::string> nums = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
        std::string line;
        for (const auto c: input) {
            if ((c >= '0' && c <= '9') || (c >= 'a' && c <= 'z')) {
                line += c;
            } else if (c == '\n') {
                auto calc = [](const auto &str) {
                    int first = 0, last = 0;
                    for (auto d: str) {
                        if (d >= '0' && d <= '9') {
                            last = d - '0';
                            if (!first) first = last;
                        }
                    }
                    return first * 10 + last;
                };
                ans1 += calc(line);

                std::string::size_type pos = 0;
                int first = 0, last = 0;
                while((pos = line.find_first_of("123456789otfsen", pos)) != std::string::npos)
                {
                    int tmp = 0;
                    if(line[pos] >= '0' && line[pos] <= '9') {
                        tmp = line[pos] - '0';
                    } else {
                        int idx = 0;
                        for(auto & s : nums) {
                            idx++;
                            if(line.find(s, pos) == pos) {
                                tmp = idx;
                                break;
                            }
                        }
                    }

                    pos++;
                    if(tmp) {
                        last = tmp;
                        if(!first) first = last;
                    }
                }
                ans2 += first * 10 + last;

                line.clear();
            }
        }

    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
