import subprocess

# Ensure this is in your PATH, or set absolute path here
picotool = 'picotool'

for page in range(2,61):
    for row in range(0,64):
        mpage = page % 3
        word = None
        if mpage == 2:   # page 2...
            if row % 2 == 1:
                word = 0xffffff
            else:
                word = 0x000000
        elif mpage == 0: # page 3...
            if row % 4 < 2:
                word = 0xffffff
            else:
                word = 0x000000
        elif mpage == 1: # page 4...
            if row % 8 < 4:
                word = 0xffffff
            else:
                word = 0x000000
        assert(word is not None)
        print(f'page {page} row {row} = {word:06x}')
        proc = [picotool, 'otp', 'set', '-r', f'{page}:{row}', f'0x{word:06x}']
        print(proc)
        subprocess.run(proc)
