#!/usr/bin/env python3

from .src import *
import time

def main():
    options, args = argsParse()
    NN_APP = NN_degenerate(seq_file=options.input, primer_length=options.plen, coverage=options.fraction,
                           number_of_dege_bases=options.dnum, score_of_dege_bases=options.degeneracy,
                           entropy_threshold=options.entropy, product_len=options.size, position=options.coordinate,
                           variation=options.variation, distance=options.away, GC=options.gc, nproc=options.proc,
                           outfile=options.out)
    NN_APP.run()


if __name__ == "__main__":
    e1 = time.time()
    main()
    e2 = time.time()
    print("INFO {} Total times: {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                                           round(float(e2 - e1), 2)))


