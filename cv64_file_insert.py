import sys
from liblzkn64 import compress_buffer

# Constants
ROM_size = [0x04004200, 0x00C00000]		# 64 MB for decompressed ROMs, 12 MB for compressed ROM
numberNIFiles = 254

# Offsets
## 0 = USA v1.0, 1 = USA v1.1, 2 = USA v1.2, 3 = JPN, 4 = EUR
NisitenmaIchigo_tableStartAddr = [0x95C34, 0x95C34, 0x95FB4, 0x979C4, 0x965B4]
fileSizeTable_startAddr = [0x95430, 0x95430, 0x957B0, 0x971C0, 0x95DB0]

# Write a file buffer to the ROM
def writeFile(romFile, inputFile, addr):
	romFile.seek(addr)
	romFile.write(inputFile)

# Patch the Nisitenma-Ichigo table entry corresponding to the file ID
# with the start and end addresses of the new injected file
# 1 entry in the table = size 0x8
def patchNITableAddresses(romFile, fileStartAddr, fileEndAddr):
	compFlagNI = 0x00000000

	tableEntryAddr = NisitenmaIchigo_tableStartAddr[version] + (8 * fileID)
	romFile.seek(tableEntryAddr)

	if compressFlag == True:
		compFlagNI = 0x80000000
	
	romFile.write((compFlagNI | fileStartAddr).to_bytes(4, 'big'))
	romFile.seek(tableEntryAddr + 4)
	romFile.write(fileEndAddr.to_bytes(4, 'big'))

# Patch table containing the file sizes with the file size of the new injected file (decompressed)
# 1 entry in the table = size 0x8
def patchFileSizeTable(romFile, fileSize):
	tableEntryAddr = fileSizeTable_startAddr[version] + (8 * fileID)
	romFile.seek(tableEntryAddr)
	segmentID = int.from_bytes(romFile.read(4), 'big') & 0xFF000000		# Get segment ID of the file
	romFile.write((segmentID | fileSize).to_bytes(4, 'big'))			# Write segment ID | file size

def checkArgsErrors():
	if compressFlag != 0 and compressFlag != 1:
			raise Exception('The "compressFlag" can only be 0 (False) or 1 (True)')
	if injectionOffset > ROM_size[compressFlag]:
			raise Exception('Invalid injection offset')
	if fileID > numberNIFiles or fileID <= 0:
			raise Exception('Invalid file ID')

def main():
	with open(romFilenameIn, "rb") as romFileIn:
		with open(romFilenameOut, "w+b") as romFileOut:
			# Copy contents of input ROM into the output ROM
			romFileOut.seek(0)
			romFileOut.write(romFileIn.read())

			# Open file to inject
			with open(filename, "rb") as fileIn:
				fileIn.seek(0)
				fileBuffer = fileIn.read()

			# Get file size of the file (decompressed),
			# which we need to patch in the file size table later
			decompressedSize = len(fileBuffer)

			# Compress the file
			if compressFlag == True:
				fileBuffer = compress_buffer(fileBuffer, False)

			# Obtain the size of the (either compressed or decompressed) file buffer
			fileBufferSize = len(fileBuffer)

			# Obtain the end address of the file and check that it doesn't surpass the end of the ROM
			fileEndAddr = injectionOffset + fileBufferSize
			if fileEndAddr > ROM_size[compressFlag]:
				raise Exception('The file to inject is too big, or it doesnt fit entirely if injected at:', hex(injectionOffset))

			writeFile(romFileOut, fileBuffer, injectionOffset)
			patchNITableAddresses(romFileOut, injectionOffset, fileEndAddr)
			patchFileSizeTable(romFileOut, decompressedSize)

if __name__ == "__main__":
	if len(sys.argv) != 8:
		print("CV64 Nisitenma-Ichigo File Injector")
		print("")
		print("python3 cv64_file_insert.py ROM_in ROM_out file_to_inject injection_address fileID compressFlag version")
		print("NOTE: All numbers are in hexadecimal, without the \"0x\"")
		print("		ROM_in: Path to the input ROM")
		print("		ROM_out: Path to the output ROM")
		print("		file_to_inject: Path to the file to be injected into the ROM")
		print("		injection_address: Address in the ROM to inject \"file_to_inject\"")
		print("		fileID: ID of the file to replace")
		print("		compressFlag: 1 to compress file, 0 to inject it decompressed")
		print("		version: CV64 version --> 0 = USA v1.0, 1 = USA v1.1, 2 = USA v1.2, 3 = JPN, 4 = EUR")

		print("\nExample: python3 cv64_file_insert.py cv64.z64 out.z64 my_new_gardener.bin BC9800 C 1 0")
		print("Injects \"my_new_gardener.bin\" into address 0xBC9800 in out.z64 (USA v1.0), replacing file 0xC. Compresses \"my_new_gardener.bin\"")
	else:
		# Arguments
		romFilenameIn = sys.argv[1]
		romFilenameOut = sys.argv[2]
		filename = sys.argv[3]
		injectionOffset = int(sys.argv[4], 16)
		fileID = int(sys.argv[5], 16)
		compressFlag = int(sys.argv[6])
		version = int(sys.argv[7])
		
		checkArgsErrors()
		main()
	