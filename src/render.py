# imaging technique:
# ion beam voltage contrast charges the word lines, causing vias to programmed bit
# cells to light up (word line shorted to bit line via blown portion of split gate)
#
# note that two bit cells share a contact (via, aka bit line), so we are actually
# seeing the OR combination of two adjacent bits on the same bit line
# they are activated by their separate word lines. for example:
# one row of bits in a bit plane:
# 'o' represents contact visible in SEM images
# '=' represents two word lines running on either side of each contact
#                                      central spine -> ||
# BL -> 28 29 30 31 27 26 25 24 20 21 22 23 19 18 17 16 || 12 13 14 15 11 10 09 08 04 05 06 07 03 02 01 00
# WL0,1 =o==o==o==o==o==o==o==o==o==o==o==o==o==o==o==o || o==o==o==o==o==o==o==o==o==o==o==o==o==o==o==o=
# so each contact represents the 'OR' combination of these bits:
# OR:   28 29 30 31 27 26 25 24 20 21 22 23 19 18 17 16    12 13 14 15 11 10 09 08 04 05 06 07 03 02 01 00
# OR:   61 62 63 64 60 59 58 57 52 53 54 55 51 50 49 48    44 45 46 47 43 42 41 40 36 37 38 39 35 34 33 32
from operator import indexOf


# logically 4096 rows across 24 bit planes
# pages are 64 bits - corresponds to 1 row in a bitplane, 2 word lines
#                                (see pvc-test8-annotated-mirrors.png)
# each bitplane is 128 rows x 32 columns
# column == bit line


# map to physical layout and display
def render(title, otp_words, wordline_seq, bitplane_seq, bitline_seq, ored=False):
    on  = 'o'
    off = '.'
    #on  = '⬢'
    #off = '⬡'
    center_spine_gap = ' ' * 33
    bitplane_gap = ' ' * 4
    if ored:
        print(f"{title} (adjacent wordlines OR'd together):")
        wordline_seq = [(wordline_seq[i],wordline_seq[i+1]) for i in range(0,len(wordline_seq),2)]
    else:
        print(f"{title}:")

    # generate header with bitplane numbers
    print('   bp: ', end='')
    for BP in bitplane_seq:
        if BP == ' ':
            print(center_spine_gap, end='')
            continue
        print(str(BP).center(33), end=bitplane_gap)
    print()

    # generate header with bitline numbers
    bl_hex_h = ''
    bl_hex_l = ''
    for BP in bitplane_seq:
        if BP == ' ':
            bl_hex_h += center_spine_gap
            bl_hex_l += center_spine_gap
            continue
        for BL in bitline_seq[BP]:
            if BL == ' ':
                bl_hex_h += ' '
                bl_hex_l += ' '
                continue
            bl_hex = f'{BL:02x}'
            bl_hex_h += bl_hex[0]
            bl_hex_l += bl_hex[1]
        bl_hex_h += bitplane_gap
        bl_hex_l += bitplane_gap
    print(f'bl(h): {bl_hex_h}')
    print(f'bl(l): {bl_hex_l}')

    # generate the array
    for WL in wordline_seq:
        if ored:
            print(f'{WL[0]:02x}|{WL[1]:02x}: ', end='')
        else:
            print(f'   {WL:02x}: ', end='')
        for BP in bitplane_seq:
            if BP == ' ':
                print(center_spine_gap, end='')
                continue
            for BL in bitline_seq[BP]:
                if BL == ' ':
                    print(' ', end='')
                    continue
                if ored:
                    bv = 0
                    for _WL in WL:
                        WL_offset = _WL * 32
                        bv |= otp_words[BP][WL_offset + BL]
                else:
                    WL_offset = WL * 32
                    bv = otp_words[BP][WL_offset + BL]
                c = on if bv == 1 else off
                print(c, end='')
            print(bitplane_gap, end='')
        print()
    print()
    print("-" * 16)
    print()


# hypothesized bit plane ordering from left to right (see fuses-angle-small-hypaddr.jpg):
bitplanes = [16,17,18,19,20,21,22,23, 0, 1, 2, 3,' ', 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]
# hypothesized bit line ordering (relative to the word line offset)
bitlines = [28,29,30,31,27,26,25,24,20,21,22,23,19,18,17,16,' ',12,13,14,15,11,10, 9, 8, 4, 5, 6, 7, 3, 2, 1, 0]
# hypothesized word line ordering (top to bottom):
wordlines = list(range(64,128)) + list(reversed(range(64)))

# all the bitlines, indexed by bitplane number
all_bitlines = {}
for i in range(24):
    if bitplanes.index(i) < 12:
        all_bitlines[i] = bitlines
    else:
        all_bitlines[i] = list(reversed(bitlines))

words = []
with open('../desired_render_words.txt', 'r') as fh:
    for line in fh:
        word = int(line, 16)
        words.append(word)
        #print(bin(word))

print(f"Loaded {len(words)} words from file")
assert(len(words) == 4096)

otp = []
# fill in the bitplane values as otp[bitplane] = ...bits...
# note these are in logical order
for bitplane in range(24):
    otp.append([])
    for bit in range(4096):
        word = words[bit]
        bit_value = 1 if word & (1 << bitplane) != 0 else 0
        otp[bitplane].append(bit_value)
    #print(otp[bitplane])


render("even wordlines", otp, wordlines[::2], bitplanes, all_bitlines, ored=False)
render("odd wordlines", otp, wordlines[1::2], bitplanes, all_bitlines, ored=False)
render("full map", otp, wordlines, bitplanes, all_bitlines, ored=True)

#eof
