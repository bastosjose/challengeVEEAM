# José Bastos
import os		
import filecmp	
import shutil	
import datetime	
import time     
import sys


# Total arguments
n = len(sys.argv)


# Checks if there's the correct number of arguments
if n != 5:

	print("Invalid number of command line arguments.\nPlease give 4 arguments - source folder path, replica folder path, synch interval (seconds), logs folder path")
	sys.exit(0)

else:

	# Directory paths
	pathSource   = sys.argv[1]+"//"
	pathReplica  = sys.argv[2]+"//"
	pathLogsFile = sys.argv[4]+"//logs.txt"


	# Synch period
	synchTime = sys.argv[3]


	while True:

		# Get the list of all files and directories in specified path
		listSource  = os.listdir(pathSource)
		listReplica = os.listdir(pathReplica)


		# Shallow compare the files in both directories
		matchSource, mismatchSource, errorsSource    = filecmp.cmpfiles(pathSource, pathReplica, listSource)
		matchReplica, mismatchReplica, errorsReplica = filecmp.cmpfiles(pathReplica, pathSource, listReplica)


		# Updates files in replica
		for i in mismatchSource:

			# Updates the file preserving the metadata
			shutil.copy2(pathSource + i, pathReplica)

			# Log with append mode
			logsFile = open(pathLogsFile, "a")
			logsFile.write("[" + str(datetime.datetime.now()) + "] - File \"" + i + "\" was updated.\n")
			logsFile.close()

			# Print to console
			print("[" + str(datetime.datetime.now()) + "] - File \"" + i + "\" was updated.\n")


		# Creates files in replica
		for i in errorsSource:

			# Copies the file preserving the metadata
			shutil.copy2(pathSource + i, pathReplica)

			# Log with append mode
			logsFile = open(pathLogsFile, "a")
			logsFile.write("[" + str(datetime.datetime.now()) + "] - File \"" + i + "\" was created.\n")
			logsFile.close()

			# Print to console
			print("[" + str(datetime.datetime.now()) + "] - File \"" + i + "\" was created.\n")


		# Deletes files in replica directory not present in the source directory
		for i in errorsReplica:

			# Deletes file
			os.remove(pathReplica + i)

			# Log with append mode
			logsFile = open(pathLogsFile, "a")
			logsFile.write("[" + str(datetime.datetime.now()) + "] - File \"" + i + "\" was deleted.\n")
			logsFile.close()

			# Print to console
			print("[" + str(datetime.datetime.now()) + "] - File \"" + i + "\" was deleted.\n")


		time.sleep(int(synchTime))