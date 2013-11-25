import sys
import getopt
from vec import Vec
from mat import Mat
from vecutil import list2vec, vec2list
from matutil import identity, listlist2mat
from GF2 import one
from math import floor

golay24mat = listlist2mat([[one, one, 0, 0, 0, one, one, one, 0, one, 0, one],
              [0, one, one, 0, 0, 0, one, one, one, 0, one, one],
              [one, one, one, one, 0, one, one, 0, one, 0, 0, 0],
              [0, one, one, one, one, 0, one, one, 0, one, 0, 0],
              [0, 0, one, one, one, one, 0, one, one, 0, one, 0],
              [one, one, 0, one, one, 0, 0, one, one, 0, 0, one],
              [0, one, one, 0, one, one, 0, 0, one, one, 0, one],
              [0, 0, one, one, 0, one, one, 0, 0, one, one, one],
              [one, one, 0, one, one, one, 0, 0, 0, one, one, 0],
              [one, 0, one, 0, one, 0, 0, one, 0, one, one, one],
              [one, 0, 0, one, 0, 0, one, one, one, one, one, 0],
              [one, 0, 0, 0, one, one, one, 0, one, 0, one, one]])

golay23mat = listlist2mat([[one, one, 0, 0, 0, one, one, one, 0, one, 0],
              [0, one, one, 0, 0, 0, one, one, one, 0, one],
              [one, one, one, one, 0, one, one, 0, one, 0, 0],
              [0, one, one, one, one, 0, one, one, 0, one, 0],
              [0, 0, one, one, one, one, 0, one, one, 0, one],
              [one, one, 0, one, one, 0, 0, one, one, 0, 0],
              [0, one, one, 0, one, one, 0, 0, one, one, 0],
              [0, 0, one, one, 0, one, one, 0, 0, one, one],
              [one, one, 0, one, one, one, 0, 0, 0, one, one],
              [one, 0, one, 0, one, 0, 0, one, 0, one, one],
              [one, 0, 0, one, 0, 0, one, one, one, one, one],
              [one, 0, 0, 0, one, one, one, 0, one, 0, one]])

def bitArrayToGF2(data):
    return [one if x==1 else 0 for x in data]

def GF2toBitArray(data):
    return [1 if x==one else 0 for x in data]


def golay24Encode(data):
    if len(data) != 12:
        return None

    # convert to a vector over GF(2)
    datavec = list2vec(bitArrayToGF2(data))
    codeword = datavec * golay24mat

    # convert codeword to bit array
    codebits = GF2toBitArray(vec2list(codeword))
    return data + codebits

def golay23Encode(data):
    if len(data) != 12:
        return None

    # convert to a vector over GF(2)
    datavec = list2vec(bitArrayToGF2(data))
    codeword = datavec * golay23mat

    # convert codeword to bit array
    codebits = GF2toBitArray(vec2list(codeword))
    return data + codebits


def ambeModGen(seed, length):
    if seed < 0 or seed > 4095:
        return None
    modVec = [16 * seed] + [0]*length
    for n in range(1, length+1):
        modVec[n] = (173 * modVec[n-1]) + 13849 - (65536 * (((173 * modVec[n-1]) + 13849) // 65536))
    modVec.pop(0)
    return [n // 32768 for n in modVec]


def dstarInterleave(blk0, blk1, blk2, blk3):
    bit_count = 0;
    bit_array = [0]*72
    
    for i in range(12):
        for j in range(6):
            bit_array[(j*12)+i] = bit_count^7;
            bit_count += 1;
    
    output = [0]*72
    counter = 0
    for i in range(24):
        output[bit_array[counter]] = blk0[i]
        counter += 1
    for i in range(23):
        output[bit_array[counter]] = blk1[i]
        counter += 1
    for i in range(11):
        output[bit_array[counter]] = blk2[i]
        counter += 1
    for i in range(14):
        output[bit_array[counter]] = blk3[i]
        counter += 1
        
    return output



# main starts here
argv = sys.argv
if len(argv) != 3:
    sys.stderr.write("Usage: %s infile.txt outfile.ambe\n" % argv[0])
    sys.exit(-1)
infile = open(argv[1], 'r')
outfile = open(argv[2], 'w')

count = 0 # loop counter used for writing out
while True:
    
    # parse a line of input
    instr = infile.readline();
    if len(instr) != 50:
        break
    # transfer the data into an array
    indata = [int(x) for x in instr if x.isdigit()]
    # break into four fields
    u0 = indata[0:12]
    u1 = indata[12:24]
    u2 = indata[24:35]
    u3 = indata[35:]
    
    # encode u0
    c0 = golay24Encode(u0)
    
    # encode u1
    intermediate_c1 = golay23Encode(u1)
    
    # apply PRNG output seeded by u0 to intermediate_c1
    seed = (u0[0] << 11 |
           u0[1] << 10 |
           u0[2] << 9  |
           u0[3] << 8  |
           u0[4] << 7  |
           u0[5] << 6  |
           u0[6] << 5  |
           u0[7] << 4  |
           u0[8] << 3  |
           u0[9] << 2  |
           u0[10] << 1 |
           u0[11])

    modArray = ambeModGen(seed, 23)
    # this is also over GF(2)
    c1 = GF2toBitArray( vec2list(list2vec(bitArrayToGF2(intermediate_c1)) + list2vec(bitArrayToGF2(modArray))))
    # just copy u2->c2 and u3->c3
    c2 = u2
    c3 = u3

    output = dstarInterleave(c0, c1, c2, c3)
    
    # convert output to a BYTE array
    byteoutput = []
    for n in range(9):
        outbyte = int(output[n*8+7]   << 7 |
                   output[n*8+6] << 6 |
                   output[n*8+5] << 5 |
                   output[n*8+4] << 4 |
                   output[n*8+3] << 3 |
                   output[n*8+2] << 2 |
                   output[n*8+1] << 1 |
                   output[n*8])
        byteoutput.append(outbyte)

    outstr = "{:05d} {:02d} {:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}".format(count // 100, count % 100, byteoutput[0], byteoutput[1], byteoutput[2], byteoutput[3], byteoutput[4], byteoutput[5], byteoutput[6], byteoutput[7], byteoutput[8])
    # write data out
    
    if(count == 0):
        outfile.write("#C Version 1.0\n")
    outfile.write(outstr)
    outfile.write("\n")
      
    count += 2
    
infile.close()
outfile.close()