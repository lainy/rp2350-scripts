import subprocess

# Ensure this is in your PATH, or set absolute path to binary here
picotool = 'picotool'

words = []
with open('../desired_render_words.txt', 'r') as fh:
    for line in fh:
        word = int(line.strip(),16)
        assert word is not None
        words.append(word)
assert(len(words) == 4096)

for page in range(2,61):
    for row in range(0,64):
        addr = (page * 64) + row
        word = words[addr]
        print(f'addr {addr:04x} ({page}:{row}) = {word:06x}')
        proc = [picotool, 'otp', 'set', '-r', f'{page}:{row}', f'0x{word:06x}']
        print(proc)
        subprocess.run(proc)

#eof
