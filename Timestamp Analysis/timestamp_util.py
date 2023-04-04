# Use this to compute the difference in time

from timestamp.py import Timestamp

# Returns the length of microseconds between the Timestamps
def get_time_difference(start_stamp: Timestamp, end_stamp: Timestamp):
	# Get difference in times
	sec_diff = end_stamp.sec - start_stamp.sec
	usec_diff = end_stamp.usec - start_stamp.usec
	
	return (sec_diff * 1000000) + usec_diff

