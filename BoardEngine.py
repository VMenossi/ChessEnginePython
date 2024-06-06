import chess
import chess.pgn
import random

num_movimentos = 0
turno = 1
tabela_tranposicao = {}


pecas = {
    "P": 10.0,   "p": -10.0,
    "N": 30.5,   "n": -30.5,
    "B": 33.3,   "b": -33.3,
    "R": 56.3,   "r": -56.3,
    "Q": 95.0,   "q": -95.0,
    "K": 900.0,  "k": -900.0
}

indices = {
    "P": 0,  "p": 1,
    "N": 2,  "n": 3,
    "B": 4,  "b": 5,
    "R": 6,  "r": 7,
    "Q": 8,  "q": 9,
    "K": 10, "k": 11
}

peao_branco_aval = [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0,
                    0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0, 0.5,
                    0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5, 0.5,
                    0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0, 0.0, 
                    0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5, 0.5,
                    1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0, 1.0, 
                    5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0, 5.0, 
                    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0]
                    
peao_preto_aval = [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0,
                   -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0, -5.0,
                   -1.0, -1.0, -2.0, -3.0, -3.0, -2.0, -1.0, -1.0, 
                   -0.5, -0.5, -1.0, -2.5, -2.5, -1.0, -0.5, -0.5, 
                   -0.0, -0.0, -0.0, -2.0, -2.0, -0.0, -0.0, -0.0, 
                   -0.5, 0.5,   1.0, -0.0, -0.0,  1.0, 0.5, -0.5, 
                   -0.5, -1.0, -1.0,  2.0,  2.0, -1.0, -1.0, -0.5, 
                   -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0]


cavalo_branco_aval =[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0, 
                     -4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0, 
                     -3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0, 
                     -3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0, 
                     -3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0, 
                     -3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0, 
                     -4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0, 
                     -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]

cavalo_preto_aval = [5.0, 4.0, 3.0, 3.0, 3.0, 3.0, 4.0, 5.0, 
                    4.0, 2.0, -0.0, -0.0, -0.0, -0.0, 2.0, 4.0, 
                    3.0, -0.0, -1.0, -1.5, -1.5, -1.0, -0.0, 3.0, 
                    3.0, -0.5, -1.5, -2.0, -2.0, -1.5, -0.5, 3.0, 
                    3.0, -0.0, -1.5, -2.0, -2.0, -1.5, -0.0, 3.0, 
                    3.0, -0.5, -1.0, -1.5, -1.5, -1.0, -0.5, 3.0, 
                    4.0, 2.0, -0.0, -0.5, -0.5, -0.0, 2.0, 4.0, 
                    5.0, 4.0, 3.0, 3.0, 3.0, 3.0, 4.0, 5.0]


bispo_branco_aval = [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
                     -1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0, 
                     -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 
                     -1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0, 
                     -1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0, 
                     -1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0, 
                     -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 
                     -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0] 

bispo_preto_aval = [2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0,
                    1.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 1.0,
                    1.0, -0.0, -0.5, -1.0, -1.0, -0.5, -0.0, 1.0, 
                    1.0, -0.5, -0.5, -1.0, -1.0, -0.5, -0.5, 1.0, 
                    1.0, -0.0, -1.0, -1.0, -1.0, -1.0, -0.0, 1.0, 
                    1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 1.0, 
                    1.0, -0.5, -0.0, -0.0, -0.0, -0.0, -0.5, 1.0, 
                    2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0]


torre_branca_aval = [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 
                    -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                    -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                    -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                    -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                    -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                    0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

torre_preta_aval = [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 
                    -0.5, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -0.5, 
                    0.5, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.5, 
                    0.5, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.5, 
                    0.5, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.5, 
                    0.5, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.5, 
                    0.5, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.5, 
                    -0.0, -0.0, -0.0, -0.5, -0.5, -0.0, -0.0, -0.0]

dama_branca_aval =[0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                  -0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5, 
                  0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

dama_preta_aval =[2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 2.0, 
                 1.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 1.0, 
                 1.0, -0.0, -0.5, -0.5, -0.5, -0.5, -0.0, 1.0, 
                 0.5, -0.0, -0.5, -0.5, -0.5, -0.5, -0.0, 0.5, 
                -0.0, -0.0, -0.5, -0.5, -0.5, -0.5, -0.0, 0.5, 
                 1.0, -0.5, -0.5, -0.5, -0.5, -0.5, -0.0, 1.0, 
                 1.0, -0.0, -0.5, -0.0, -0.0, -0.0, -0.0, 1.0, 
                 2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 2.0]


rei_branco_aval = [2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0, 2.0, 
                   2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0, 2.0, 
                  -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0, 
                  -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
                  -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0, 
                  -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0, 
                  -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0, 
                  -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0]

rei_preto_aval = [3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0, 
                  3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0, 
                  3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0, 
                  3.0, 4.0, 4.0, 5.0, 5.0, 4.0, 4.0, 3.0, 
                  2.0, 3.0, 3.0, 4.0, 4.0, 3.0, 3.0, 2.0, 
                  1.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 1.0, 
                 -2.0, -2.0, -0.0, -0.0, -0.0, -0.0, -2.0, -2.0, 
                 -2.0, -3.0, -1.0, -0.0, -0.0, -1.0, -3.0, -2.0]

peao_branco_aval_final = [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0,
                           -1.5, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.5,
                            0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5, 0.5,
                            0.5,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, 0.5, 
                            0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0, 0.0,
                            1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, 1.0, 
                            3.0,  3.0,  3.0,  3.0,  3.0,  3.0,  3.0, 3.0, 
                            0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0]

peao_preto_aval_final = [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 
                         -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, -3.0, 
                         -1.0, -0.5, -0.5, -1.0, -1.0, -0.5, -0.5, -1.0, 
                         -0.0, -0.0, -0.0, -0.5, -0.5, -0.0, -0.0, -0.0, 
                         -0.5, -0.5, -0.5, -1.0, -1.0, -0.5, -0.5, -0.5, 
                         -0.5, 0.5, 1.0, -0.0, -0.0, 1.0, 0.5, -0.5, 
                         1.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 
                         -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0]

cavalo_branco_aval_final =[ -2.5, -2.0, -1.5, -1.5, -1.5, -1.5, -2.0, -2.5, 
                            -2.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.0, -2.0, 
                            -1.5,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -1.5, 
                            -1.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -1.0, 
                            -1.0,  1.0,  1.5,  2.0,  2.0,  1.5,  1.0, -1.0, 
                            -1.5,  1.0,  2.0,  1.5,  1.5,  2.0,  1.0, -1.5, 
                            -2.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -2.0, 
                            -2.5, -2.0, -1.5, -1.5, -1.5, -1.5, -2.0, -2.5]

cavalo_preto_aval_final = [2.5, 2.0, 1.5, 1.5, 1.5, 1.5, 2.0, 2.5, 
                           2.0, -0.0, -1.0, -1.5, -1.5, -1.0, -0.0, 2.0, 
                           1.5, -1.0, -2.0, -1.5, -1.5, -2.0, -1.0, 1.5, 
                           1.0, -1.0, -1.5, -2.0, -2.0, -1.5, -1.0, 1.0, 
                           1.0, -0.5, -1.5, -2.0, -2.0, -1.5, -0.5, 1.0, 
                           1.5, -0.0, -1.0, -1.5, -1.5, -1.0, -0.0, 1.5, 
                           2.0, 0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 2.0, 
                           2.5, 2.0, 1.5, 1.5, 1.5, 1.5, 2.0, 2.5]

bispo_branco_aval_final = [ -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 
                            -1.0,  1.5,  1.5,  1.5,  1.5,  1.5,  1.5, -1.0, 
                            -1.0,  1.5,  2.0,  2.0,  2.0,  2.0,  1.5, -1.0, 
                            -1.0,  1.5,  2.0,  2.0,  2.0,  2.0,  1.5, -1.0, 
                            -1.0,  1.5,  1.5,  1.5,  1.5,  1.5,  1.5, -1.0, 
                            -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0, 
                            -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0, 
                            -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0] 

bispo_preto_aval_final = [ -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 
                            -1.0,  1.5,  1.5,  1.5,  1.5,  1.5,  1.5, -1.0, 
                            -1.0,  1.5,  2.0,  2.0,  2.0,  2.0,  1.5, -1.0, 
                            -1.0,  1.5,  2.0,  2.0,  2.0,  2.0,  1.5, -1.0, 
                            -1.0,  1.5,  1.5,  1.5,  1.5,  1.5,  1.5, -1.0, 
                            -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0, 
                            -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0, 
                            -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0] 

torre_branca_aval_final = [  1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 
                             0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 
                             0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 
                             0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 
                             0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 
                             0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0, 
                             1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 
                             1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

torre_preta_aval_final = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 
                          -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, 
                          -0.0, -0.0, -0.0, -0.5, -0.5, -0.0, -0.0, -0.0, 
                          -0.0, -0.0, -0.0, -0.5, -0.5, -0.0, -0.0, -0.0, 
                          -0.0, -0.0, -0.0, -0.5, -0.5, -0.0, -0.0, -0.0, 
                          -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 
                          -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 
                          -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]

dama_branca_aval_final =[   0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                            0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 
                            0.5, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, 0.5, 
                            0.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0, 
                            0.0, 1.0, 1.0, 2.0, 2.0, 1.0, 1.0, 1.0,  
                            0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,  
                            1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 
                            1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

dama_preta_aval_final = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 
                         -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, 
                         -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 
                         -1.0, -1.0, -1.0, -2.0, -2.0, -1.0, -1.0, -0.0, 
                         -1.0, -1.0, -1.0, -2.0, -2.0, -1.0, -1.0, -0.0, 
                         -0.5, -0.5, -1.0, -1.5, -1.5, -1.0, -0.5, -0.5, 
                         -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 
                         -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0]

rei_branco_aval_final = [   -1.0, -1.0, -0.5, -0.5, -0.5, -0.5, -1.0, -1.0, 
                            -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5, 
                             0.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -0.0, 
                             0.0,  1.0,  1.5,  2.0,  2.0,  1.5,  1.0, 0.0, 
                             0.0,  1.0,  1.5,  2.0,  2.0,  1.5,  1.0, 0.0, 
                             0.0,  0.0,  2.0,  1.5,  1.5,  2.0,  0.0, 0.0, 
                             0.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0,  0.0, 
                             0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0]

rei_preto_aval_final = [-0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 
                        -0.0, -0.0, -1.0, -1.5, -1.5, -1.0, -0.0, -0.0, 
                        -0.0, -0.0, -2.0, -1.5, -1.5, -2.0, -0.0, -0.0, 
                        -0.0, -1.0, -1.5, -2.0, -2.0, -1.5, -1.0, -0.0, 
                        -0.0, -1.0, -1.5, -2.0, -2.0, -1.5, -1.0, -0.0, 
                        0.0, -0.0, -1.0, -1.5, -1.5, -1.0, -0.0, -0.0, 
                        0.5, -0.0, -0.0, -0.0, -0.0, -0.0, -0.0, 0.5, 
                        1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 1.0]

aval_pos = [peao_branco_aval, peao_preto_aval, cavalo_branco_aval, cavalo_preto_aval, bispo_branco_aval, bispo_preto_aval,
            torre_branca_aval, torre_preta_aval, dama_branca_aval, dama_preta_aval, rei_branco_aval, rei_preto_aval]

aval_pos_final = [peao_branco_aval_final, peao_preto_aval_final, cavalo_branco_aval_final, cavalo_preto_aval_final, bispo_branco_aval_final, bispo_preto_aval_final,
            torre_branca_aval_final, torre_preta_aval_final, dama_branca_aval_final, dama_preta_aval_final, rei_branco_aval_final, rei_preto_aval_final]

def avaliarPos(tabuleiro):
    aval = 0
    
    for tipo in range(1,7):
        for cor in [True,False]:
            casas = tabuleiro.pieces(tipo,cor)
            for casa in casas:
                peca = tabuleiro.piece_at(casa).symbol()
                if(len(casas)<15):
                    aval += pecas[peca] + aval_pos_final[indices[peca]][casa]
                else:
                    aval += pecas[peca] + aval_pos[indices[peca]][casa] 
    return aval

def OrdemDeMovimentos(tabuleiro):
    cheques = [] 
    capturas = []
    outros = []
    ordem = []
    for jogada in list(tabuleiro.legal_moves):
        if tabuleiro.gives_check(jogada):
            cheques.append(jogada)
        elif (tabuleiro.is_capture(jogada)):
            capturas.append(jogada)
        else:
            outros.append(jogada)
    ordem = cheques + capturas + outros
    return ordem

def capturasCheques(tabuleiro):
    ordem = []
    for jogada in list(tabuleiro.legal_moves):
        if tabuleiro.gives_check(jogada) or tabuleiro.is_capture(jogada):
            ordem.append(jogada)
    return ordem

def quiescence(tabuleiro, profundidade, jogadorMax, alfa, beta):
    global num_movimentos,tabela_tranposicao
    chave = str(tabuleiro.fen())
    if chave not in tabela_tranposicao:
        num_movimentos += 1

        if tabuleiro.is_checkmate():
            if jogadorMax:
                tabela_tranposicao[chave] = float('-inf')
                return float('-inf'),profundidade
            tabela_tranposicao[chave] = float('inf')
            return float('inf'),profundidade

        if (tabuleiro.is_insufficient_material() or tabuleiro.is_stalemate() or tabuleiro.is_repetition(3) or tabuleiro.is_fifty_moves()) :
            tabela_tranposicao[chave] = 0
            return 0,profundidade

        capturas_cheques = capturasCheques(tabuleiro)
        if len(capturas_cheques) == 0:
            aux = avaliarPos(tabuleiro)
            tabela_tranposicao[chave] = aux
            return aux,profundidade
            
        if jogadorMax:
            melhor = float('-inf')
            for jogada in capturas_cheques:
                tabuleiro.push(jogada)
                valor, profun= quiescence(tabuleiro, profundidade - 1, False, alfa, beta)
                tabuleiro.pop()
                melhor = max(melhor, valor)
                alfa = max(alfa, melhor)
                if beta <= alfa :
                    break
            return melhor,profun
        else:
            melhor = float('inf')
            for jogada in capturas_cheques:
                tabuleiro.push(jogada)
                valor,profun = alfaBeta(tabuleiro, profundidade - 1, True, alfa, beta)
                tabuleiro.pop()
                melhor = min(melhor, valor)
                beta = min(beta, melhor)
                if beta <= alfa:
                    break
            return melhor,profun
    return tabela_tranposicao[chave],profundidade
        
            

def melhorMovimento(tabuleiro, profundidade, jogadorMax):
    global tabela_tranposicao, num_movimentos
    tabela_tranposicao = {}
    melhor_profun = float('-inf')
    if jogadorMax:
        melhor_aval = float('-inf')
    else:
        melhor_aval = float('inf')

    for jogada in OrdemDeMovimentos(tabuleiro):
        num_movimentos += 1
        tabuleiro.push(jogada)
        valor,aux_profun = alfaBeta(tabuleiro, profundidade -1, not jogadorMax, float("-inf"), float("inf"))
        tabuleiro.pop()
        if jogadorMax:
            if valor > melhor_aval:
                melhor_aval = valor
                melhor_profun = aux_profun
                melhor_movimento = jogada
            elif valor == melhor_aval and aux_profun > melhor_profun:
                melhor_profun = aux_profun
                melhor_movimento = jogada
        else:
            if valor < melhor_aval:
                melhor_aval = valor
                melhor_profun = aux_profun
                melhor_movimento = jogada
            elif valor == melhor_aval and aux_profun > melhor_profun:
                melhor_profun = aux_profun
                melhor_movimento = jogada
    
    return melhor_movimento


#Corte alfa-beta
def alfaBeta(tabuleiro, profundidade, jogadorMax, alfa, beta):
    global num_movimentos,tabela_tranposicao
    chave = str(tabuleiro.fen())
    if chave not in tabela_tranposicao:
        num_movimentos += 1

        if tabuleiro.is_checkmate():
            if jogadorMax:
                tabela_tranposicao[chave] = float('-inf')
                return float('-inf'),profundidade
            tabela_tranposicao[chave] = float('inf')

            return float('inf'),profundidade

        if (tabuleiro.is_insufficient_material() or tabuleiro.is_stalemate() or tabuleiro.is_repetition(3) or tabuleiro.is_fifty_moves()) :
            tabela_tranposicao[chave] = 0

            return 0,profundidade
        
        if (profundidade == 0):
            aux = avaliarPos(tabuleiro)
            tabela_tranposicao[chave] = aux

            return quiescence(tabuleiro,profundidade,jogadorMax,alfa,beta)

        if jogadorMax:
            melhor = float('-inf')
            for jogada in OrdemDeMovimentos(tabuleiro):
                tabuleiro.push(jogada)
                valor, profun= alfaBeta(tabuleiro, profundidade - 1, False, alfa, beta)
                tabuleiro.pop()
                melhor = max(melhor, valor)
                alfa = max(alfa, melhor)
                if beta <= alfa :
                    break
            return melhor,profun
        else:
            melhor = float('inf')
            for jogada in OrdemDeMovimentos(tabuleiro):
                tabuleiro.push(jogada)
                valor,profun = alfaBeta(tabuleiro, profundidade - 1, True, alfa, beta)
                tabuleiro.pop()
                melhor = min(melhor, valor)
                beta = min(beta, melhor)
                if beta <= alfa:
                    break
            return melhor,profun
    return tabela_tranposicao[chave],profundidade

def CCA(tabuleiro):
    cheques = [] 
    capturas = []
    ataques = [] 
    outros = []
    ordem = []
    for jogada in list(tabuleiro.legal_moves):
        if tabuleiro.gives_check(jogada):
            cheques.append(jogada)
        elif (tabuleiro.is_capture(jogada)):
            capturas.append(jogada)
        else:
            tabuleiro.push(jogada)
            if len(tabuleiro.attacks(jogada.to_square)) != 0:
                ataques.append(jogada)
            else:
                outros.append(jogada)
            tabuleiro.pop()
    ordem = cheques + capturas + ataques + outros
    if(len(cheques) + len(capturas) == 0):
        return random.choice(ordem)
    return ordem[0]

def minimizarMovimentos(tabuleiro):
    menor = float('inf')
    for jogada in list(tabuleiro.legal_moves):
        tabuleiro.push(jogada)
        if menor > tabuleiro.legal_moves.count():
            menor = tabuleiro.legal_moves.count()
            lance_min = jogada
        tabuleiro.pop()
    print("Numero de movimentos do adversario:", menor)
    return lance_min

def humano(tabuleiro):
    while True:
        print("DIGITE SEU MOVIMENTO:")
        jogada = str(input())
        jogada = chess.Move.from_uci(jogada)
        if jogada not in tabuleiro.legal_moves:
            print("MOVIMENTO IMPOSSIVEL")
        else:
            return jogada

def main():
    global turno
    tabuleiro = chess.Board()
    jogo = chess.pgn.Game()
    profundidade = 0
    opt = 0
    while opt != 1 and opt != 2:
        print("HUMANO CONTRA MAQUINA - DIGITE 1")
        print("MAQUINA X MAQUINA     - DIGITE 2")
        opt = int(input())
    print("DIGITE A PRONFUDIDADE DESEJADA:")
    profundidade = int(input())
    if opt == 1:
        opt = 0
        while opt != 1 and opt != 2:
            print("SELECIONE SUA COR: \n BRANCAS - DIGITE 1 \n PRETAS - DIGITE 2")
            opt = int(input())
            if opt == 1:
                print(tabuleiro.unicode())
                movimento = humano(tabuleiro)
                turno += 1
                no = jogo.add_variation(movimento)
                tabuleiro.push(movimento)
                print("\n")
                print(tabuleiro.unicode())
                print(tabuleiro.fen())

                while not (tabuleiro.is_game_over()):
                    if turno % 2 != 0:
                        movimento = humano(tabuleiro)
                    else:
                        print("PENSANDO...")
                        movimento = melhorMovimento(tabuleiro,profundidade,False)
                    turno += 1
                    no = no.add_variation(movimento)
                    tabuleiro.push(movimento)
                    print("\n")
                    print(tabuleiro.unicode())
                    print(tabuleiro.fen())
                print(jogo)
            elif opt == 2:
                print(tabuleiro.unicode())
                print("PENSANDO...")
                movimento = melhorMovimento(tabuleiro,profundidade,True)
                turno += 1
                no = jogo.add_variation(movimento)
                tabuleiro.push(movimento)
                print("\n")
                print(tabuleiro.unicode())
                print(tabuleiro.fen())

                while not (tabuleiro.is_game_over()):
                    if turno % 2 != 0:
                        print("PENSANDO...")
                        movimento = melhorMovimento(tabuleiro,profundidade,True)
                    else:
                        movimento = humano(tabuleiro)
                    turno += 1
                    no = no.add_variation(movimento)
                    tabuleiro.push(movimento)
                    print("\n")
                    print(tabuleiro.unicode())
                    print(tabuleiro.fen())
            print(jogo)
    elif opt == 2:
        opt = 0
        while opt != 1 and opt != 2 and opt != 3:
            print("CCA X ALFA-BETA       - digite 1")
            print("MinMov x ALFA-BETA    - digite 2")
            print("ALFA-BETA X ALFA-BETA - digite 3")
            # print("HUMANO X MinMov       - digite 4")
            # print("MinMOV X CCA          - digite 5")
            opt = int(input())
            if(opt == 1):
                print(tabuleiro.unicode())
                movimento = CCA(tabuleiro)
                turno += 1
                no = jogo.add_variation(movimento)
                tabuleiro.push(movimento)
                print("\n")
                print(tabuleiro.unicode())
                print(tabuleiro.fen())

                while not (tabuleiro.is_game_over()):
                    if turno % 2 != 0:
                        movimento = CCA(tabuleiro)
                    else:
                        movimento = melhorMovimento(tabuleiro, profundidade, False)
                    turno += 1
                    no = no.add_variation(movimento)
                    tabuleiro.push(movimento)
                    print("\n")
                    print(tabuleiro.unicode())
                    print(tabuleiro.fen())
                print(jogo)
            elif opt == 2 :
                print(tabuleiro.unicode())
                movimento = minimizarMovimentos(tabuleiro)
                turno += 1
                no = jogo.add_variation(movimento)
                tabuleiro.push(movimento)
                print("\n")
                print(tabuleiro.unicode())
                print(tabuleiro.fen())

                while not (tabuleiro.is_game_over()):
                    if turno % 2 != 0:
                        movimento = minimizarMovimentos(tabuleiro)
                    else:
                        movimento = melhorMovimento(tabuleiro, profundidade, False)
                    turno += 1
                    no = no.add_variation(movimento)
                    tabuleiro.push(movimento)
                    print("\n")
                    print(tabuleiro.unicode())
                    print(tabuleiro.fen())
                print(jogo)
            elif opt == 3:
                print(tabuleiro.unicode())
                movimento = melhorMovimento(tabuleiro, profundidade, True)
                turno += 1
                no = jogo.add_variation(movimento)
                tabuleiro.push(movimento)
                print("\n")
                print(tabuleiro.unicode())
                print(tabuleiro.fen())

                while not (tabuleiro.is_game_over()):
                    if turno % 2 != 0:
                        movimento = melhorMovimento(tabuleiro, profundidade, True)
                    else:
                        movimento = melhorMovimento(tabuleiro, profundidade, False)
                    turno += 1
                    no = no.add_variation(movimento)
                    tabuleiro.push(movimento)
                    print("\n")
                    print(tabuleiro.unicode())
                    print(tabuleiro.fen())
                print(jogo)
            # elif opt == 4:
            #     print(tabuleiro.unicode())
            #     movimento = humano(tabuleiro)
            #     turno += 1
            #     no = jogo.add_variation(movimento)
            #     tabuleiro.push(movimento)
            #     print("\n")
            #     print(tabuleiro.unicode())
            #     print(tabuleiro.fen())

            #     while not (tabuleiro.is_game_over()):
            #         if turno % 2 != 0:
            #             movimento = humano(tabuleiro)
            #         else:
            #             movimento = minimizarMovimentos(tabuleiro)
            #         turno += 1
            #         no = no.add_variation(movimento)
            #         tabuleiro.push(movimento)
            #         print("\n")
            #         print(tabuleiro.unicode())
            #         print(tabuleiro.fen())
            #     print(jogo)
            # elif opt == 5:
            #     print(tabuleiro.unicode())
            #     movimento = minimizarMovimentos(tabuleiro)
            #     turno += 1
            #     no = jogo.add_variation(movimento)
            #     tabuleiro.push(movimento)
            #     print("\n")
            #     print(tabuleiro.unicode())
            #     print(tabuleiro.fen())

            #     while not (tabuleiro.is_game_over()):
            #         if turno % 2 != 0:
            #             movimento = minimizarMovimentos(tabuleiro)
            #         else:
            #             movimento = CCA(tabuleiro)
            #         turno += 1
            #         no = no.add_variation(movimento)
            #         tabuleiro.push(movimento)
            #         print("\n")
            #         print(tabuleiro.unicode())
            #         print(tabuleiro.fen())
            #     print(jogo)

main()