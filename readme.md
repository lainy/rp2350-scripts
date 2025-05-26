This repository contains scripts and fuse data used in IOActive's RP2350
antifuse research.

The associated paper can be found here:
- https://arxiv.org/abs/2501.13276

Script usage:
- `render.py` - Reads OTP fuse dump from `desired_render_words.txt`, outputs
  ASCII art of the fuse values. Can be used to obtain ASCII art of a fuse dump
  for comparison with PVC images.
- `fuse_from_render.py` - Reads ASCII art from `desired_render.txt` and outputs
  fuse values which will produce a PVC image of the desired ASCII art. Output
  of this is piped to `desired_render_words.txt` for use with `burn_fuses_from_file.py`
- `burn_fuses_from_file.py` - Reads words from `desired_render_words.txt`, calls
  [picotool](https://github.com/raspberrypi/picotool) to burn the data into OTP.

Files:
- `desired_render.txt` - ASCII art to be converted to fuse values. Note that
  all bits are present in this file, not just the bitwise OR of adjacent bits
  as seen by the PVC technique described in the paper.
- `desired_render_words.txt` - Fuse values generated from `desired_render.txt`
- `desired_render_output.txt` - ASCII art reconstructed from `desired_render_words.txt`
  for testing the entire flow. Shows the bitwise OR of adjacent bitcells which
  share a via, to match what is seen in PVC imaging.

The following command sequence (\*nix shell) was used to dump the words burned
into an RP2350:
```sh
picotool otp get -r `seq 0 4095` | grep '^ \+VALUE 0x' | cut -d' ' -f6
```

