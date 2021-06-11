/** $lic$
 * Copyright (C) 2016-2017 by Massachusetts Institute of Technology
 *
 * This file is part of TailBench.
 *
 * If you use this software in your research, we request that you reference the
 * TaiBench paper ("TailBench: A Benchmark Suite and Evaluation Methodology for
 * Latency-Critical Applications", Kasture and Sanchez, IISWC-2016) as the
 * source in any publications that use this software, and that you send us a
 * citation of your work.
 *
 * TailBench is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.
 */

#ifndef __DIST_H
#define __DIST_H

#include <random>
#include <stdint.h>

class Dist {
    public:
        virtual ~Dist() {};
        virtual uint64_t nextArrivalNs() = 0;
};

class ExpDist : public Dist {
    private:
        std::default_random_engine g;
        std::exponential_distribution<double> d;
        uint64_t curNs;
        uint64_t nextSleepNs; 
        uint64_t sleepNs;
        uint64_t burstNs;

    public:
        ExpDist(double lambda, uint64_t seed, uint64_t startNs, uint64_t sleepNs, uint64_t burstNs) 
            : g(seed), d(lambda), curNs(startNs),nextSleepNs(startNs + burstNs), sleepNs(sleepNs), burstNs(burstNs) {}

        uint64_t nextArrivalNs() {
            curNs += d(g);

            //gspark
            if(burstNs != 0 && sleepNs != 0)
                if( curNs > nextSleepNs )
                {
                    curNs += sleepNs;
                    nextSleepNs = curNs + burstNs;
                    //std::cout << "next sleep time: " << nextSleepNs << std::endl;
                }

            return curNs;
        }
};

#endif
