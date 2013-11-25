
bit_count = 0;
bit_array = [0]*72

for i in range(12):
    for j in range(6):
        bit_array[(j*12)+i] = bit_count^7;
        bit_count++;