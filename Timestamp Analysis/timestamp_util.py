# Use this to compute the difference in time

from timestamp import Timestamp

from datetime import datetime, timedelta


# Returns the length of microseconds between the Timestamps
def get_time_difference(start_stamp: Timestamp, end_stamp: Timestamp):
	# Get difference in times
	sec_diff = end_stamp.sec - start_stamp.sec
	usec_diff = end_stamp.usec - start_stamp.usec
	
	# print(start_stamp.to_string() + ", " + end_stamp.to_string() + ", " + str((sec_diff * 1000000) + usec_diff))
	
	return (sec_diff * 1000000) + usec_diff


# Returns a list of timestamp objects from report_log.txt in the same directory
# Raises an exception in event of an error
def get_timestamps():
	line_number = 1
	timestamp_list = []
	
	# Open the file
	file = open('report_log.txt', 'r')
	if file.closed:
		raise Exception("Unable to open log.txt")
	
	# Create a Timestamp for each object
	line = file.readline().strip() # returns "" if empty
	while line:
		# Check line length
		if len(line) < 15:
			raise Exception("Error: Insufficient number of characters on line " + str(line_number) + ", actual: " + str(len(line)) + ", expected: >= 15")
		
		code = line[0:3]
		if not code.isalpha():
			raise Exception("Error: Code is not alphabetical: " + code)
		
		semicolon_index = line.find(":")
		if semicolon_index == -1:
			raise Exception("Error: \':\' not found on line " + str(line_number))
		
		sec = line[4:semicolon_index]
		usec = line[(semicolon_index + 1):len(line)]
		
		timestamp_list.append(Timestamp(code, int(sec), int(usec)))
		
		# For next iteration
		line = file.readline().strip()
		line_number += 1
	
	file.close()
	
	return sorted(timestamp_list, key=_compare_timestamps)
	
# Get a datetime object used to sort the list of timestamps
def _compare_timestamps(timestamp):
	return datetime.fromtimestamp(timestamp.sec) + timedelta(microseconds=timestamp.usec)

