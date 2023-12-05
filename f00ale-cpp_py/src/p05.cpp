#include "aoc.h"
#include <vector>
#include <algorithm>
#include <iostream>
#include <tuple>
#include <set>

std::tuple<std::string, std::string> p05(const std::string &input) {
    int64_t ans1 = 0;
    int64_t ans2 = 0;

    std::vector<int64_t> seeds;
    std::vector<std::vector<std::tuple<int64_t, int64_t, int64_t>>> maps;
    {
        bool have_seeds = false;
        int64_t num = 0;
        bool havenum = false;
        std::vector<int64_t> row;
        for (const auto c: input) {
            if (c >= '0' && c <= '9') {
                num *= 10;
                num += c - '0';
                havenum = true;
            } else {
                if(havenum) {
                    if(!have_seeds) {
                        seeds.push_back(num);
                    } else {
                        row.push_back(num);
                    }
                }
                if(c == ':' && have_seeds) {
                    maps.emplace_back();
                }
                if(c == '\n') {
                    if(have_seeds) {
                        if(row.size() == 3) {
                            maps.back().emplace_back(row[0], row[1], row[2]);
                        }
                    }
                    row.clear();
                    have_seeds = true;
                }
                havenum = false;
                num = 0;
            }
        }

    }


    ans1 = std::numeric_limits<int64_t>::max();
    ans2 = std::numeric_limits<int64_t>::max();

    for(auto & m: maps) {
        std::sort(m.begin(), m.end(), [](const auto & m1, const auto & m2) { return std::get<1>(m1) < std::get<1>(m2); });
    }

//    for(auto s : seeds) std::cout << s << ' '; std::cout << '\n';
//    for(auto & m : maps) {
//        for(auto [d,s,l] : m) std::cout << d << ' ' << s << ' ' << l << '\n';
//        std::cout << '\n';
//    }

    for(auto seed : seeds) {
            for (auto &m: maps) {
                for (auto [dest, src, len]: m) {
                    if (seed >= src && seed < src + len) {
                        seed = dest + seed - src;
                        break;
                    }
                }
            }
            if (seed < ans1) ans1 = seed;
    }

    for(int i = 0; i < seeds.size(); i+=2) {
        std::vector<std::tuple<int64_t, int64_t>> pairs;
        pairs.emplace_back(seeds[i], seeds[i+1]); //??
        for(const auto & m : maps) {
            std::vector<std::tuple<int64_t, int64_t>> newpairs;
            for(auto [seedstart, seedlen] : pairs) {
                for(auto [dest, src, len] : m) {
                    auto overlap = [](int64_t min1, int64_t max1, int64_t min2, int64_t max2) {
                        return std::max(int64_t(0), std::min(max1, max2) - std::max(min1,min2));
                    };
                    auto ol = overlap(seedstart, seedstart+seedlen, src, src+len);
                    if(ol) {
                        if(seedstart >= src) newpairs.emplace_back(dest+seedstart-src, ol);
                        else newpairs.emplace_back(dest+src-seedstart, ol);
                    }
                }
            }
            pairs.swap(newpairs);
//            for(auto [s,l] : pairs) {
//                std::cout << s << ' ' << l << '\n';
//            }
        }
        for(auto[seed, l] : pairs) {
            if(seed < ans2) ans2 = seed;
        }
    }


    return {std::to_string(ans1), std::to_string(ans2)};
}
