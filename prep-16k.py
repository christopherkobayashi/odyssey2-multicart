#! /usr/bin/env python

import os
from sys import argv

script, infile = argv
outfile = infile+'-16k'

rom_table = bytearray( 16384 )

with open(infile, "rb") as binaryfile:
  in_rom = bytearray(binaryfile.read())
binaryfile.close()

size = len(in_rom)
print ("ROM:", infile, "size:", size, "banks:", int(size / 2048))

if size == 2048:
  # bank 0 (mirror for missing A10)
  rom_table[0x0400:0x0c00] = in_rom[0x0000:0x0800]
  rom_table[0x0c00:0x1000] = rom_table[0x0800:0x0c00]
  # copy up to 16k image size
  rom_table[0x1000:0x2000] = rom_table[0x0000:0x1000]
  rom_table[0x2000:0x4000] = rom_table[0x0000:0x2000]

elif size == 4096:
  # bank 0 (mirror for missing A10)
  rom_table[0x0400:0x0c00] = in_rom[0x0000:0x0800]
  rom_table[0x0c00:0x1000] = rom_table[0x0800:0x0c00]
  # bank 1 (mirror for missing A10)
  rom_table[0x1400:0x1c00] = in_rom[0x0800:0x1000]
  rom_table[0x1c00:0x2000] = rom_table[0x1800:0x1c00]
  # copy up to 16k image size
  rom_table[0x2000:0x4000] = rom_table[0x0000:0x2000]

elif size == 8192:
  # bank 0 (mirror for missing A10)
  rom_table[0x0400:0x0c00] = in_rom[0x0000:0x0800]
  rom_table[0x0c00:0x1000] = rom_table[0x0800:0x0c00]
  # bank 1 (mirror for missing A10)
  rom_table[0x1400:0x1c00] = in_rom[0x0800:0x1000]
  rom_table[0x1c00:0x2000] = rom_table[0x1800:0x1c00]
  # bank 2 (mirror for missing A10)
  rom_table[0x2400:0x2c00] = in_rom[0x1000:0x1800]
  rom_table[0x2c00:0x3000] = rom_table[0x2800:0x2c00]
  # bank 3 (mirror for missing A10)
  rom_table[0x3400:0x3c00] = in_rom[0x1800:0x2000]
  rom_table[0x3c00:0x4000] = rom_table[0x3800:0x3c00]

else:
  print("error: can't handle anything bigger than 8k")
  sys.exit()

with open(outfile, "wb") as out_rom:
  out_rom.write(rom_table)
out_rom.close()
