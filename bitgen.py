
import itertools
# Fffffff = f0 fundamental frequency; (tone frame if Vv is 11 and Ffff are all 1111, see below)
# Vvvv(v) = voiced/unvoiced states
# Ggggg(g) = gain
# Mmmmmmmmm = PRBA13 Spectral
# Nnnnnnn = PRBA47 Spectral
# Pppp(p) = HOC0 Spectral
# Qqqq = HOC1 Spectral
# Rrrr = HOC2 Spectral
# Sss = HOC3 Spectral

# fixed frame length to 48 bits:
#  INDX           000000000011111111112222222222333333333344444444
#  indx           012345678901234567890123456789012345678901234567
# Bit meanings:   FfffffGgggMmmmmmmNnnnnPpppQqqqRrrrSssVvvvggmmnnf
#   Cx block#     000000000000111111111111222222222222222223333333
#   sorted        FffffffVvvvGgggggMmmmmmmmmNnnnnnnPpppQqqqRrrrSss



freq = [0, 1, 1, 1, 0, 0, 1]

gain = [0, 1, 0, 1, 1, 1]

m = [0]*9
n = [0]*7
p = [0]*4
q = [0]*4
r = [0]*4
s = [0]*3

# generate list of all possible v/uv values

vuv_vals = list(itertools.product([0,1], [0,1], repeat=2))

for val in vuv_vals:
    v = list(val)
    for j in range(0,32):
        out_dat = freq[:6] + gain[:4] + m[:7] + n[:5] + p + q + r + s + v + gain[4:] + m[7:] + n[5:] + freq[6:]
        # convert to string
        outs = "".join(map(str,out_dat))
        print(outs)