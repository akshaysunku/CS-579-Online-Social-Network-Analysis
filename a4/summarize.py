"""
Summarize data.
"""
def write_summary():
	""" write the summary of the data collected, clustering and classification
	into summary.txt
	"""
	print("Started Writing to summary.txt")

	file = open('summary.txt', 'w')

	file1 = open("./Collect Data/collect_summary.txt", 'r')
	file.write("Collected Data Summary\n")
	file.write("-----------------------\n")
	file.write(file1.read())
	file.write('\n')
	file1.close()
	
	file2 = open("./Cluster/cluster_summary.txt", 'r')
	file.write("Cluster Summary\n")
	file.write("----------------\n")
	file.write(file2.read())
	file.write('\n')
	file2.close()

	file3 = open("./Classify/classification_summary.txt", 'r')
	file.write("Classification Summary\n")
	file.write("-----------------------\n")
	file.write(file3.read())
	file.write('\n')
	file2.close()

	print("Finished Writing to summary.txt")

def main():
	write_summary()
	pass

if __name__ == "__main__":
    main()