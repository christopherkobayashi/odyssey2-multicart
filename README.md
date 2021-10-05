# Simple Odyssey2/Videopac multicart

This is a simple manually-switched Odyssey2/Videopac multicart.  DIP switches select from one of 32 cartridge banks.

The hardware design is not mine.  It is courtesy
[Wilco2008's blog](https://web.archive.org/web/20210601074542/https://wilco2009.blogspot.com/2018/09/videopac-multirom-cart-version-1.html).

The multicart Eagle schematic and board files are in the eagle/ subdirectory.  Gerber files suitable for fabrication from PCBway are in the gerber/ subdirectory.

The EEPROM is a Winbond 29C040, which are readily available on the secondary market.  The resisters are typical 1/4 watt pulldowns; I used 4.7k because I had them lying around.  The capacitor is a 0.1uF non-polarized ceramic.

Wilco2008 provided a Windows binary to convert o2em ROM files into 16k images suitable for each bank.  Unfortunately, the binary doesn't work (it appears to FTP to a site that doesn't exist anymore, and then quits immediately).  Source code is unavailable.

Happily, the ROM memory layout is documented in this post at the
[Videopac Forum](http://videopac.nl/forum/index.php?topic=1778.0).  The python script `prep-16k.py` will assemble a bank-switched image from an input file.

The code from the forum post is below.

```
	nb=size/1024;  // find out number of kbytes to load

        switch (nb){
            case 2: // 2 k cartridge no A10
                    printf("Loading %d blocks of 1k\n\r",nb);

                    fread(&rom_buffer[0x0400],2048,1,fp);                       // read 2k block at 0x0400
                    memcpy(&rom_buffer[0x0c00],&rom_buffer[0x0800],1024);       // mirror to 0x0C00 (ignore A10)           
                    
                    memcpy(&rom_buffer[0x1000],&rom_buffer[0x0000],4096);       // mirror (ignore P10)
                    memcpy(&rom_buffer[0x2000],&rom_buffer[0x0000],8192);       // mirror (ignore P11)

                    break;
            case 4: // 4 k cartridge no A10, ROM_A11=CPU_P10, ROM_A10=CPU_A11 ignore P11
                    // after RESET P10 (and P11) will be high so a fetch from the CPU 
                    // from 0x0400 will be from physical (EP)ROM address 0x0800
                    printf("Loading %d blocks of 1k\n\r",nb);

                    fread(&rom_buffer[0x0400],2048,1,fp);                       // read 2k block at 0x0400
                    memcpy(&rom_buffer[0x0C00],&rom_buffer[0x0800],1024);       // mirror to 0x0C00 (ignore A10)           

                    fread(&rom_buffer[0x1400],2048,1,fp);                       // read 2k block at 0x1400 
                    memcpy(&rom_buffer[0x1C00],&rom_buffer[0x1800],1024);       // mirror to 0x1C00 (ignore A10)    
                    
                    memcpy(&rom_buffer[0x2000],&rom_buffer[0x0000],8192);       // mirror (ignore P11)
                    
                    break;
            case 8: // 8 k cartridge no A10 bank select with P10 and P11 (A12 and A13)
                    fread(&rom_buffer[0x0400],2048,1,fp);                       // read 2k block at 0x0400
                    memcpy(&rom_buffer[0x0C00],&rom_buffer[0x0800],1024);       // mirror to 0x0C00 (ignore A10)           

                    fread(&rom_buffer[0x1400],2048,1,fp);                       // read 2k block at 0x1400 
                    memcpy(&rom_buffer[0x1C00],&rom_buffer[0x1800],1024);       // mirror to 0x1C00 (ignore A10)   

                    fread(&rom_buffer[0x2400],2048,1,fp);                       // read 2k block at 0x2400
                    memcpy(&rom_buffer[0x2C00],&rom_buffer[0x2800],1024);       // mirror to 0x2C00 (ignore A10)           

                    fread(&rom_buffer[0x3400],2048,1,fp);                       // read 2k block at 0x3400 
                    memcpy(&rom_buffer[0x3C00],&rom_buffer[0x3800],1024);       // mirror to 0x3C00 (ignore A10)   
                    
                    break;
            default:// unknown size
                    printf("Panic!\n\rUnknown rom size\n\r");
                    break;
        }
```


