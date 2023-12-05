#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p02(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    {
        int num = 0;
        bool havenum = false;
        int mr = 0, mg = 0, mb = 0;
        int game = 0, lastnum = 0;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else {
                if(havenum) {
                    if (game) {
                        lastnum = num;
                    } else {
                        game = num;
                    }
                    havenum = false;
                    num = 0;
                }
                if(lastnum && (c == 'r' || c == 'g' || c == 'b')) {
                    if(c == 'r') mr = std::max(mr, lastnum);
                    if(c == 'g') mg = std::max(mg, lastnum);
                    if(c == 'b') mb = std::max(mb, lastnum);
                    lastnum = 0;
                }
                if(c == '\n') {
                    if(mr <= 12 && mg <= 13 && mb <= 14) {
                        ans1 += game;
                    }
                    ans2 += mr*mg*mb;
                    game = mr = mg = mb = 0;
                }
            }
        }

    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
