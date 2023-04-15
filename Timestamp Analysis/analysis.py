from timestamp_util import get_time_difference
from timestamp_util import get_timestamps
from timestamp_util import reorder_ties_given_priority
from timestamp_util import get_average
from timestamp import Timestamp

import traceback


# REC printed in osi.c osi() after line "num_fd_events = epoll_wait(ctx->epoll_fd, epoll_events, NUM_EVENT_TYPES, -1);"
# CFM printed in osi.c osi_process_encrypted_event() after line "} else if (ev->value != 0) {"
# END printed in osi_gui_base.py process_text_message() after line "self.text.insert(INSERT, chr(c))"
def time_keystroke_to_plaintext_in_gui(timestamp_list):
	# Correctly order REC and CFM when they have the same timestamp
	reorder_ties_given_priority(timestamp_list, "REC", "CFM")			
	
	duration_list = []
	for stamp_index in range(len(timestamp_list)):
		start_stamp = timestamp_list[stamp_index]
		# if the stamp is a REC
		if start_stamp.code == "REC":
			if (stamp_index + 1) < len(timestamp_list):
				# if the next one is CFM
				if timestamp_list[stamp_index + 1].code == "CFM":
					# the next should be END
					#assert (stamp_index + 2 < len(timestamp_list)), "Reached end of list without the expected END stamp"
					#end_stamp = timestamp_list[stamp_index + 2]
					#assert (end_stamp.code == "END"), "Expecting an END stamp on line: " + str(stamp_index + 2)
					#duration_list.append(get_time_difference(start_stamp, end_stamp))
					if (stamp_index + 2 < len(timestamp_list)):
						end_stamp = timestamp_list[stamp_index + 2]
						if (end_stamp.code == "END"):
							duration_list.append(get_time_difference(start_stamp, end_stamp))
	
	# Get the first 1000 elements
	if len(duration_list) > 1000:
		duration_list = duration_list[:1000]
	
	# Print useful info
	print("timestamp_list length: " +str(len(timestamp_list)))
	print("duration_list length: " + str(len(duration_list)))
	for duration in duration_list:
		print(str(duration))
		
	cfm_count = 0
	end_count = 0
	for i in range(len(timestamp_list)):
		if timestamp_list[i].code == "CFM":
			cfm_count += 1
		if timestamp_list[i].code == "END":
			end_count += 1
	print("CFM count: " + str(cfm_count))
	print("END count: " + str(end_count))
	
	print("Average time from keypress to gui: " + str(get_average(duration_list)))

# REC printed in osi.c osi() after line "num_fd_events = epoll_wait(ctx->epoll_fd, epoll_events, NUM_EVENT_TYPES, -1);"
# LSN printed in osi.c osi() after loop "for (i = 0; i < num_fd_events; ++i) { ... }"
def time_process_input_pre_encryption(timestamp_list):
	# Correctly order REC and CFM when they have the same timestamp
	reorder_ties_given_priority(timestamp_list, "REC", "LSN")
	
	duration_list = []
	for stamp_index in range(len(timestamp_list)):
		if timestamp_list[stamp_index].code == "REC":
			if stamp_index < len(timestamp_list) - 1:
				if timestamp_list[stamp_index + 1].code == "LSN":
					duration_list.append(get_time_difference(timestamp_list[stamp_index], timestamp_list[stamp_index + 1]))
	
	# Get the first 1000 elements
	if len(duration_list) > 1000:
		duration_list = duration_list[:1000]
	
	# Print useful info
	print("timestamp_list length: " + str(len(timestamp_list)))
	print("duration_list length: " + str(len(duration_list)))
	for duration in duration_list:
		print(str(duration))
		
	rec_count = 0
	lsn_count = 0
	for i in range(len(timestamp_list)):
		if timestamp_list[i].code == "REC":
			rec_count += 1
		if timestamp_list[i].code == "LSN":
			lsn_count += 1
	print("REC count: " + str(rec_count))
	print("LSN count: " + str(lsn_count))
	
	print("Average time to process a keypress while not in encrypt mode: " + str(get_average(duration_list)))

# BEG printed in osi_crypto_provider.c before XOR loop in function osi_stream_encrypt()
# END printed in osi_crypto_provider.c after XOR loop in function osi_stream_encrypt()
def time_xor_encrypt(timestamp_list):
	# Correctly order BEC and END when they have the same timestamp
	reorder_ties_given_priority(timestamp_list, "BEG", "END")

	duration_list = []
	for stamp_index in range(len(timestamp_list)):
		if timestamp_list[stamp_index].code == "BEG":
			if stamp_index < len(timestamp_list) - 1:
				if timestamp_list[stamp_index + 1].code == "END":
					duration_list.append(get_time_difference(timestamp_list[stamp_index], timestamp_list[stamp_index + 1]))

	# Print useful info
	print("timestamp_list length: " + str(len(timestamp_list)))
	for timestamp in timestamp_list:
		print(timestamp.to_string())
	print("duration_list length: " + str(len(duration_list)))
	for duration in duration_list:
		print(str(duration))
		
	print("Average time to perform an XOR: " + str(get_average(duration_list)))
	

def main():
	timestamp_list = None
	
	try:
		timestamp_list = get_timestamps()
	except Exception as e:
		print("Error: Unable to load timestamps: " + str(e))
		traceback.print_exc()
	
	#for timestamp in timestamp_list:
	#	print(timestamp.to_string())
	
	#time_keystroke_to_plaintext_in_gui(timestamp_list)
	#time_process_input_pre_encryption(timestamp_list)
	time_xor_encrypt(timestamp_list)
		
	print("DONE")
	
if __name__ == "__main__":
	main()

