# CV64 File Insert
Python script to replace files referenced in the Nisitenma-Ichigo table from Castlevania (Nintendo 64).

## Prerequisites
```sh
pip install numpy
```
```sh
pip install numba
```

## Usage
```
CV64 Nisitenma-Ichigo File Injector

python3 cv64_file_insert.py ROM_in ROM_out file_to_inject injection_address fileID compressFlag version
NOTE: All numbers are in hexadecimal, without the "0x"
                ROM_in: Path to the input ROM
                ROM_out: Path to the output ROM
                file_to_inject: Path to the file to be injected into the ROM
                injection_address: Address in the ROM to inject "file_to_inject"
                fileID: ID of the file to replace
                compressFlag: 1 to compress file, 0 to inject it decompressed
                version: CV64 version --> 0 = USA v1.0, 1 = USA v1.1, 2 = USA v1.2, 3 = JPN, 4 = EUR

Example: python3 cv64_file_insert.py cv64.z64 out.z64 my_new_gardener.bin BC9800 C 1 0
Injects "my_new_gardener.bin" into address 0xBC9800 in out.z64 (USA v1.0), replacing file 0xC. Compresses "my_new_gardener.bin"
```

## Credits
- [@Fluvian](https://github.com/Fluvian) and [@LiquidCat64](https://github.com/LiquidCat64)
for reversing the [LZKN64](https://github.com/Fluvian/lzkn64) compression algorithm used by Konami