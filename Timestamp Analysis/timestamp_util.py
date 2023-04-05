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


# Reorders ties for time in the list, edits the list and returns nothing
def reorder_ties_given_priority(timestamp_list: list[Timestamp], first_code: str, second_code: str):
	for i in range(len(timestamp_list)):
		if i < (len(timestamp_list) - 1):
			# There is a following element
			if timestamp_list[i].sec == timestamp_list[i + 1].sec and timestamp_list[i].usec == timestamp_list[i + 1].usec:
				# The they have the same time
				if timestamp_list[i].code == second_code and timestamp_list[i + 1].code == first_code:
					temp_timestamp = timestamp_list[i]
					timestamp_list[i] = timestamp_list[i + 1]
					timestamp_list[i + 1] = temp_timestamp
	


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
	
# returns the average of each int in a list of ints
def get_average(duration_list: int):
	total = 0
	
	for duration in duration_list:
		total += duration
	
	return total / len(duration_list)

# Get a datetime object used to sort the list of timestamps
def _compare_timestamps(timestamp):
	return datetime.fromtimestamp(timestamp.sec) + timedelta(microseconds=timestamp.usec)
	

