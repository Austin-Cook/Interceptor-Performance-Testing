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
					# Ignore bug where BEG prints after END
					duration_list.append(get_time_difference(timestamp_list[stamp_index], timestamp_list[stamp_index + 1]))

	# Get the first 1000 elements
	if len(duration_list) > 1000:
		duration_list = duration_list[:1000]

	# Print useful info
	print("timestamp_list length: " + str(len(timestamp_list)))
	for timestamp in timestamp_list:
		print(timestamp.to_string())
	print("duration_list length: " + str(len(duration_list)))
	for duration in duration_list:
		print(str(duration))
		
	print("Average time to perform an XOR: " + str(get_average(duration_list)))
	
	
def time_modify_one_time_pad(timestamp_list):
	# Correctly order BEC and END when they have the same timestamp
	reorder_ties_given_priority(timestamp_list, "BEG", "END")

	duration_list = []
	for stamp_index in range(len(timestamp_list)):
		if timestamp_list[stamp_index].code == "BEG":
			if stamp_index < len(timestamp_list) - 1:
				if timestamp_list[stamp_index + 1].code == "END":
					# Ignore bug where BEG prints after END
					duration_list.append(get_time_difference(timestamp_list[stamp_index], timestamp_list[stamp_index + 1]))

	# Get the first 1000 elements
	if len(duration_list) > 1000:
		duration_list = duration_list[:1000]

	# Print useful info
	print("timestamp_list length: " + str(len(timestamp_list)))
	for timestamp in timestamp_list:
		print(timestamp.to_string())
	print("duration_list length: " + str(len(duration_list)))
	for duration in duration_list:
		print(str(duration))
		
	print("Average time to create or update the one time pad: " + str(get_average(duration_list)))

# REC printed in osi.c osi() after line "num_fd_events = epoll_wait(ctx->epoll_fd, epoll_events, NUM_EVENT_TYPES, -1);"
# CFM printed in osi.c osi_process_encrypted_event() after line "} else if (ev->value != 0) {"
# END printed in osi_encrypt.c osi_process_new_plaintext() after line "rc = osi_kbd_virt_write_base64_string( ... )"
def time_keystroke_to_destination_encrypted(timestamp_list):
	# Correctly order REC and CFM when they have the same timestamp
	reorder_ties_given_priority(timestamp_list, "REC", "CFM")			
	
	# Remove all REC that don't have CFM after
	indexes_to_remove = []
	for stamp_index in range(len(timestamp_list)):
		if timestamp_list[stamp_index].code == "REC":
			if not ((stamp_index < len(timestamp_list) - 1) and (timestamp_list[stamp_index + 1].code == "CFM")):
				indexes_to_remove.append(stamp_index)
	for index_to_remove in reversed(indexes_to_remove):
		timestamp_list.pop(index_to_remove)
	
	# For each remaining REC, if END is 2 after, use the REC and END times
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
	
	# Get the first 500 elements
	if len(duration_list) > 500:
		duration_list = duration_list[:500]
	
	# Print useful info
	print("timestamp_list length: " + str(len(timestamp_list)))
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
	
	print("Average time from keypress to destination: " + str(get_average(duration_list)))
	if len(duration_list) >= 10:
		print("Average time for 1st 10: " + str(get_average(duration_list[:10])))
		if len(duration_list) >= 50:
			print("Average time for 1st 50: " + str(get_average(duration_list[:50])))
			if len(duration_list) >= 100:
				print("Average time for 1st 100: " + str(get_average(duration_list[:100])))
				if len(duration_list) >= 200:
					print("Average time for 1st 200: " + str(get_average(duration_list[:200])))
					if len(duration_list) >= 500:
						print("Average time for 1st 500: " + str(get_average(duration_list[:500])))
	if len(duration_list) >= 50:
		print("Average time for 11-50: " + str(get_average(duration_list[10:50])))
		if len(duration_list) >= 100:
			print("Average time for 51-100: " + str(get_average(duration_list[50:100])))
			if len(duration_list) >= 200:
				print("Average time for 101-200: " + str(get_average(duration_list[100:200])))
				if len(duration_list) >= 500:
					print("Average time for 201-500: " + str(get_average(duration_list[200:500])))
					print("Average time for 201-300: " + str(get_average(duration_list[200:300])))
					print("Average time for 301-400: " + str(get_average(duration_list[300:400])))
					print("Average time for 401-500: " + str(get_average(duration_list[400:500])))

# BEG printed in osi_gui_encrypt.py function finish_encryption() ln 368
# END printed in 
def time_overlay_submit_plaintext_to_destination(timestamp_list):
	
			

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
	#time_xor_encrypt(timestamp_list)
	#time_modify_one_time_pad(timestamp_list)
	time_keystroke_to_destination_encrypted(timestamp_list)
		
	print("DONE")
	
if __name__ == "__main__":
	main()

