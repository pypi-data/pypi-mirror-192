#!/usr/bin/env python3

from optparse import OptionParser
import numpy as np
import sys
import math
from operator import mul
from math import log10
from functools import reduce


# Melting temperature between 55-80◦C reduces the occurrence of hairpins
# Runs of three or more Cs or Gs at the 3'-ends of primers may promote mispriming at G or C-rich sequences
# (because of stability of annealing), and should be avoided.
def argsParse():
    parser = OptionParser('Usage: %prog -i input -o output -p 10\n \
                Options: { -l [18] -n [4] -d [10] -v [1] -g [0.2,0.7] -f [0.8] -c [4] -p [10] -a [4] }')
    parser.add_option('-i', '--input',
                      dest='input',
                      help='Input file: multi-alignment output (muscle or others).')

    parser.add_option('-l', '--plen',
                      dest='plen',
                      default=18,
                      type="int",
                      help='Length of primer. Default: 18.')

    parser.add_option('-n', '--dnum',
                      dest='dnum',
                      default=4,
                      type="int",
                      help='Number of degenerate. Default: 4.')

    parser.add_option('-d', '--degeneracy',
                      dest='degeneracy',
                      default=10,
                      type="int",
                      help='degeneracy of primer. Default: 10.')

    parser.add_option('-v', '--variation',
                      dest='variation',
                      default=1,
                      type="int",
                      help='Max mismatch number of primer. Default: 1.')

    parser.add_option('-e', '--entropy',
                      dest='entropy',
                      default=3.6,
                      type="float",
                      help='Entropy is actually a measure of disorder. This parameter is used to judge whether the '
                           'window is conservation. Entropy of primer-length window. Default: 3.6.')

    parser.add_option('-g', '--gc',
                      dest='gc',
                      default="0.2,0.7",
                      help="Filter primers by GC content. Default [0.2,0.7].")

    parser.add_option('-s', '--size',
                      dest='size',
                      default="100",
                      type="int",
                      help="Filter primers by mini PRODUCT size. Default 100.")

    parser.add_option('-f', '--fraction',
                      dest='fraction',
                      default="0.8",
                      type="float",
                      help="Filter primers by match fraction. If you set -s lower than 0.8, make sure that "
                           "--entropy greater than 3.6, because disorder region (entropy > 3.6) will not be processed "
                           "in multiPrime. Even these regions can design coverage with error greater than your "
                           "threshold, it wont be processed. Default: 0.8.")

    parser.add_option('-c', '--coordinate',
                      dest='coordinate',
                      default="4",
                      type="int",
                      help="Mismatch index is not allowed to locate in start or stop. "
                           "otherwise, it won't be regard as the mis-coverage. "
                           "With this param, you can control the index of Y-distance (number=variation and position of mismatch) "
                           "when calculate coverage with error."
                           "Default: 4.")

    parser.add_option('-p', '--proc',
                      dest='proc',
                      default="20",
                      type="int",
                      help="Number of process to launch. Default: 20.")

    parser.add_option('-a', '--away',
                      dest='away',
                      default=4,
                      help='Filter hairpin structure, which means distance of the minimal paired bases. Default: 4. '
                           'Example:(number of X) AGCT[XXXX]AGCT. '
                           'Primers should not have complementary sequences (no consecutive 4 bp complementarities),'
                           'otherwise the primers themselves will fold into hairpin structure.')

    parser.add_option('-o', '--out',
                      dest='out',
                      help='Output file: candidate primers. e.g. [*].candidate.primers.txt.')
    (options, args) = parser.parse_args()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    elif options.input is None:
        parser.print_help()
        print("Input file must be specified !!!")
        sys.exit(1)
    elif options.out is None:
        parser.print_help()
        print("No output file provided !!!")
        sys.exit(1)
    return parser.parse_args()


degenerate_base = {"-": ["-"], "A": ["A"], "G": ["G"], "C": ["C"], "T": ["T"], "R": ["A", "G"], "Y": ["C", "T"],
                   "M": ["A", "C"], "K": ["G", "T"], "S": ["G", "C"], "W": ["A", "T"], "H": ["A", "T", "C"],
                   "B": ["G", "T", "C"], "V": ["G", "A", "C"], "D": ["G", "A", "T"], "N": ["A", "T", "G", "C"]}

score_table = {"-": 100, "#": 0, "A": 1, "G": 1.11, "C": 1.21, "T": 1.4, "R": 2.11, "Y": 2.61, "M": 2.21,
               "K": 2.51, "S": 2.32, "W": 2.4, "H": 3.61, "B": 3.72, "V": 3.32, "D": 3.51, "N": 4.72}

trans_score_table = {v: k for k, v in score_table.items()}

##############################################################################################
############################# Calculate free energy ##########################################
##############################################################################################
freedom_of_H_37_table = [[-0.7, -0.81, -0.65, -0.65],
                         [-0.67, -0.72, -0.8, -0.65],
                         [-0.69, -0.87, -0.72, -0.81],
                         [-0.61, -0.69, -0.67, -0.7]]

penalty_of_H_37_table = [[0.4, 0.575, 0.33, 0.73],
                         [0.23, 0.32, 0.17, 0.33],
                         [0.41, 0.45, 0.32, 0.575],
                         [0.33, 0.41, 0.23, 0.4]]

H_bonds_number = [[2, 2.5, 2.5, 2],
                  [2.5, 3, 3, 2.5],
                  [2.5, 3, 3, 2.5],
                  [2, 2.5, 2.5, 2]]
adjust_initiation = {"A": 0.98, "T": 0.98, "C": 1.03, "G": 1.03}
adjust_terminal_TA = 0.4
# Symmetry correction applies only to self-complementary sequences.
# symmetry_correction = 0.4
symmetry_correction = 0.4

##############################################################################################
base2bit = {"A": 0, "C": 1, "G": 2, "T": 3, "#": 4}
TRANS = str.maketrans("ATCG", "TAGC")

def complement(seq):
    return seq.translate(TRANS)[::-1]



##############################################################################################
# 37°C and 1 M NaCl
Htable2 = [[-7.9, -8.5, -8.2, -7.2, 0],
           [-8.4, -8, -9.8, -8.2, 0],
           [-7.8, -10.6, -8, -8.5, 0],
           [-7.2, -7.8, -8.4, -7.9, 0],
           [0, 0, 0, 0, 0]]
Stable2 = [[-22.2, -22.7, -22.2, -21.3, 0],
           [-22.4, -19.9, -24.4, -22.2, 0],
           [-21, -27.2, -19.9, -22.7, 0],
           [-20.4, -21, -22.4, -22.2, 0],
           [0, 0, 0, 0, 0]]
Gtable2 = [[-1, -1.45, -1.3, -0.58, 0],
           [-1.44, -1.84, -2.24, -1.3, 0],
           [-1.28, -2.17, -1.84, -1.45, 0],
           [-0.88, -1.28, -1.44, -1, 0],
           [0, 0, 0, 0, 0]]
H_adjust_initiation = {"A": 2.3, "T": 2.3, "C": 0.1, "G": 0.1}
S_adjust_initiation = {"A": 4.1, "T": 4.1, "C": -2.8, "G": -2.8}
G_adjust_initiation = {"A": 1.03, "T": 1.03, "C": 0.98, "G": 0.98}
H_symmetry_correction = 0
S_symmetry_correction = -1.4
G_symmetry_correction = 0.4
##############################################################################################
# ng/ul
primer_concentration = 100
Mo_concentration = 50
Di_concentration = 1.5
dNTP_concentration = 0.25
Kelvin = 273.15
# reference (Owczarzy et al.,2008)
crossover_point = 0.22

bases = np.array(["A", "C", "G", "T"])
di_bases = []
for i in bases:
    for j in bases:
        di_bases.append(i + j)


def Penalty_points(length, GC, d1, d2):
    return log10((2 ** length * 2 ** GC) / ((d1 + 0.1) * (d2 + 0.1)))


di_nucleotides = set()
for i in base2bit.keys():
    single = i * 4
    di_nucleotides.add(single)
    for j in base2bit.keys():
        if i != j:
            di = (i + j) * 4
            di_nucleotides.add(di)
        for k in base2bit.keys():
            if i != j != k:
                tri = (i + j + k) * 3
                di_nucleotides.add(tri)

TRANS = str.maketrans("ATGCRYMKSWHBVDN", "TACGYRKMSWDVBHN")


def score_trans(sequence):
    return reduce(mul, [math.floor(score_table[x]) for x in list(sequence)])


def dege_number(sequence):
    return sum(math.floor(score_table[x]) > 1 for x in list(sequence))


def RC(seq):
    return seq.translate(TRANS)[::-1]


##############################################################################################
############## m_distance which is used to calculate (n)-nt variation coverage ###############
# Caution: this function only works when degeneracy of seq2 < 2 (no degenerate in seq2).
##############################################################################################
def Y_distance(seq1, seq2):
    seq_diff = list(np.array([score_table[x] for x in list(seq1)]) - np.array([score_table[x] for x in list(seq2)]))
    m_dist = [idx for idx in range(len(seq_diff)) if seq_diff[idx] not in score_table.values()]
    return m_dist


##############################################################################################
def symmetry(seq):
    if len(seq) % 2 == 1:
        return False
    else:
        F = seq[:int(len(seq) / 2)]
        R = complement(seq[int(len(seq) / 2):][::-1])
        if F == R:
            return True
        else:
            return False


def Calc_deltaH_deltaS(seq):
    Delta_H = 0
    Delta_S = 0
    for n in range(len(seq) - 1):
        i, j = base2bit[seq[n + 1]], base2bit[seq[n]]
        Delta_H += Htable2[i][j]
        Delta_S += Stable2[i][j]
    seq = seq.replace("#", '')
    Delta_H += H_adjust_initiation[seq[0]] + H_adjust_initiation[seq[-1]]
    Delta_S += S_adjust_initiation[seq[0]] + S_adjust_initiation[seq[-1]]
    if symmetry(seq):
        Delta_S += S_symmetry_correction
    return Delta_H * 1000, Delta_S


# salt_adjust = math.log(Tm_Na_adjust / 1000.0, math.e)
# def S_adjust(seq):
#     n = len(seq) - 1
#     # S_Na_adjust = 0.847 * n * salt_adjust
#     # Oligonucleotide Melting Temperatures under PCR Conditions: Nearest-Neighbor Corrections for
#     # Mg2+ , Deoxynucleotide Triphosphate, and Dimethyl Sulfoxide Concentrations with
#     # Comparison to Alternative Empirical Formulas
#     S_Na_adjust = 0.368 * n * salt_adjust
#     # A unified view of polymer, dumbbell, and oligonucleotide DNA nearest-neighbor thermodynamics
#     return S_Na_adjust
# where n is the total number of phosphates in the duplex divided by 2,
# This is equal to the oligonucleotide length minus 1.

def GC_fraction(seq):
    return round((list(seq).count("G") + list(seq).count("C")) / len(list(seq)), 3)


# different salt corrections for monovalent (Owczarzy et al.,2004) and divalent cations (Owczarzy et al.,2008)
def Calc_Tm_v2(seq):
    delta_H, delta_S = Calc_deltaH_deltaS(seq)
    # Note that the concentrations in the following Eq is mmol/L, In all other equations,concentration are mol/L
    # Monovalent cations are typically present as K+ and Tris+ in PCR buffer,
    # K+ is similar to Na+ in regard to duplex stabilization
    # if Di_concentration > dNTP_concentration:
    #     Tm_Na_adjust = Mo_concentration + 120 * math.sqrt(Di_concentration - dNTP_concentration)
    # else:
    #     Tm_Na_adjust = Mo_concentration
    Tm_Na_adjust = Mo_concentration

    if dNTP_concentration >= Di_concentration:
        free_divalent = 0.00000000001
    else:
        free_divalent = (Di_concentration - dNTP_concentration) / 1000.0
    R_div_monov_ratio = (math.sqrt(free_divalent)) / (Mo_concentration / 1000)

    if R_div_monov_ratio < crossover_point:
        # use only monovalent salt correction, [equation 22] (Owczarzy et al., 2004)
        correction = (((4.29 * GC_fraction(seq)) - 3.95) * pow(10, -5) * math.log(Tm_Na_adjust / 1000.0, math.e)) \
                     + (9.40 * pow(10, -6) * (pow(math.log(Tm_Na_adjust / 1000.0, math.e), 2)))
    else:
        # magnesium effects are dominant, [equation 16] (Owczarzy et al., 2008) is used
        # Table 2
        a = 3.92 * pow(10, -5)
        b = - 9.11 * pow(10, -6)
        c = 6.26 * pow(10, -5)
        d = 1.42 * pow(10, -5)
        e = - 4.82 * pow(10, -4)
        f = 5.25 * pow(10, -4)
        g = 8.31 * pow(10, -5)
        if R_div_monov_ratio < 6.0:
            a = 3.92 * pow(10, -5) * (
                    0.843 - (0.352 * math.sqrt(Tm_Na_adjust / 1000.0) * math.log(Tm_Na_adjust / 1000.0, math.e)))
            d = 1.42 * pow(10, -5) * (
                    1.279 - 4.03 * pow(10, -3) * math.log(Tm_Na_adjust / 1000.0, math.e) - 8.03 * pow(10, -3) * pow(
                math.log(Tm_Na_adjust / 1000.0, math.e), 2))
            g = 8.31 * pow(10, -5) * (
                    0.486 - 0.258 * math.log(Tm_Na_adjust / 1000.0, math.e) + 5.25 * pow(10, -3) * pow(
                math.log(Tm_Na_adjust / 1000.0, math.e), 3))
        # Eq 16
        correction = a + (b * math.log(free_divalent, math.e))
        + GC_fraction(seq) * (c + (d * math.log(free_divalent, math.e)))
        + (1 / (2 * (len(seq) - 1))) * (e + (f * math.log(free_divalent, math.e))
                                        + g * (pow((math.log(free_divalent, math.e)), 2)))

    if symmetry(seq):
        # Equation A
        Tm = round(1 / ((1 / (delta_H / (delta_S + 1.9872 * math.log(primer_concentration / (1 * pow(10, 9)), math.e))))
                        + correction) - Kelvin, 2)
    else:
        # Equation B
        Tm = round(1 / ((1 / (delta_H / (delta_S + 1.9872 * math.log(primer_concentration / (4 * pow(10, 9)), math.e))))
                        + correction) - Kelvin, 2)
    return Tm


##############################################################################################
