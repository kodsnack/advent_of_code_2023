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

    decltype(maps) newmap;
    for(auto & m: maps) {
        int64_t last = 0;
        newmap.emplace_back();
        for(auto [d,s,l] : m) {
            if(last < s) {
                newmap.back().emplace_back(last,last,s-last);
            }
            newmap.back().emplace_back(d,s,l);
            last = s+l;
        }
        newmap.back().emplace_back(last,last,std::numeric_limits<int64_t>::max()-last);
    }

    maps.swap(newmap);

    for(auto p : {1, 2}) {
        for (decltype(seeds)::size_type i = 0; i < seeds.size(); i += p) {
            std::vector<std::tuple<int64_t, int64_t>> pairs;
            pairs.emplace_back(seeds[i], (p == 1 ? 1 : seeds[i + 1])); //??
            for (const auto &m: maps) {
                std::vector<std::tuple<int64_t, int64_t>> newpairs;
                for (auto [seedstart, seedlen]: pairs) {
                    if(seedlen <= 0) break;
                    for (auto [dest, src, len]: m) {
                        auto overlap = [](int64_t min1, int64_t max1, int64_t min2, int64_t max2) {
                            return std::max(int64_t(0), std::min(max1, max2) - std::max(min1, min2));
                        };
                        auto ol = overlap(seedstart, seedstart + seedlen, src, src + len);
                        if (ol) {
                            int64_t newstart = 0;
                            if (seedstart > src) newstart = dest + seedstart - src;
                            else newstart = dest + src - seedstart;
                            newpairs.emplace_back(newstart, ol);
                        }
                        seedlen -= ol;
                        seedstart+=ol;
                    }
                }
                pairs.swap(newpairs);
            }
            for (auto [seed, l]: pairs) {
                auto &ans = (p == 1 ? ans1 : ans2);
                if (seed < ans) ans = seed;
            }
        }
    }

    return {std::to_string(ans1), std::to_string(ans2)};
}
