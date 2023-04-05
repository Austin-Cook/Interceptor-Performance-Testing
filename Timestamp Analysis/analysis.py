from timestamp_util import get_time_difference
from timestamp_util import get_timestamps
from timestamp import Timestamp

import traceback


# REC printed in osi.c osi() after line "num_fd_events = epoll_wait(ctx->epoll_fd, epoll_events, NUM_EVENT_TYPES, -1);"
# CFM printed in osi.c osi_process_encrypted_event() after line "} else if (ev->value != 0) {"
# END printed in osi_gui_base.py process_text_message() after line "self.text.insert(INSERT, chr(c))"
def time_keystroke_to_plaintext_in_gui(timestamp_list):
	duration_list = []
	

	
	for stamp_index in range(len(timestamp_list)):
		start_stamp = timestamp_list[stamp_index]
		# if the stamp is a REC
		if start_stamp.code == "REC":
			if (stamp_index + 1) < len(timestamp_list):
				# if the next one is CFM
				if timestamp_list[stamp_index + 1].code == "CFM":
					# the next should be END
					if (stamp_index + 2 < len(timestamp_list)):
						end_stamp = timestamp_list[stamp_index + 2]
						if (end_stamp.code == "END"):
							duration_list.append(get_time_difference(start_stamp, end_stamp))
	
	print("timestamp_list length: " +str(len(timestamp_list)))
	print("duration_list length: " + str(len(duration_list)))
	for duration in duration_list:
		print(str(duration))


def main():
	timestamp_list = None
	
	try:
		timestamp_list = get_timestamps()
	except Exception as e:
		print("Error: Unable to load timestamps: " + str(e))
		traceback.print_exc()
	
	for timestamp in timestamp_list:
		print(timestamp.to_string())
	
	time_keystroke_to_plaintext_in_gui(timestamp_list)
		
	print("DONE")
	
if __name__ == "__main__":
	main()

