bitplanes = []
bitlines = []
wordlines = {}
with open('../desired_render.txt', 'r') as fh:
    line = fh.readline().strip()
    bitplanes = [x for x in line.split(' ') if x != '']
    assert(bitplanes[0] == 'bp:')
    bitplanes = bitplanes[1:]
    bitplanes = [int(x) for x in bitplanes]
    assert(len(bitplanes) == 24)

    line = fh.readline().strip()
    assert(line[0:6] == 'bl(h):')
    bl_h = line[6:].replace(' ', '')
    assert(len(bl_h) == 768)

    line = fh.readline().strip()
    assert(line[0:6] == 'bl(l):')
    bl_l = line[6:].replace(' ', '')
    assert(len(bl_l) == 768)

    for i in range(len(bl_l)):
        bitlines.append(int(f'{bl_h[i]}{bl_l[i]}', 16))

    for line in fh:
        wordline, bits = line.strip().replace(' ', '').split(':')
        wordline = int(wordline, 16)
        assert(len(bits) == 768)
        bits = bits.replace('.', '0')
        bits = bits.replace('o', '1')
        wordlines[wordline] = bits

words = [0] * 4096
for wl, bits in wordlines.items():
    wl_offset = wl * 32
    for i, bit in enumerate(bits):
        bl = bitlines[i]
        bp = bitplanes[int(i / 32)]
        value = int(bit) << bp
        #print((wl_offset + bl), wl, bl, bp, bit, value)
        words[wl_offset + bl] += value

for word in words:
    print(f'0x{word:06x}')

#eof
