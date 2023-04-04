# Use these functions to make an asynchronous POST request to the server

#include <curl/curl.h>
#include <pthread.h>
#include <syslog.h>
#include <time.h>


// Helper function to run on separate thread
void *_log_time(void *code) {
	CURL *curl;
	CURLcode res;

	// Get the code
	char *identifier = (char *)code;

	// Get the time
	struct timeval now;
	gettimeofday(&now, NULL);

	// Create the json object
	char *unfilledJson =
			"{ \"identifier\": \"%s\", \"time\": { \"sec\": \"%ld\", \"usec\": \"%ld\" } }";
	char jsonObjString[300];
	sprintf(jsonObjString, unfilledJson, identifier, now.tv_sec, now.tv_usec);

	curl = curl_easy_init();
	if (curl) {
		// Fill the headers
		struct curl_slist *headers = NULL;
		headers = curl_slist_append(headers, "Accept: application/json");
		headers = curl_slist_append(headers, "Content-Type: application/json");
		headers = curl_slist_append(headers, "charset: utf-8");

		curl_easy_setopt(curl, CURLOPT_URL, "http://localhost:4560/report");
		// Specify the POST data
		curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, jsonObjString);

		// Perform the request
		res = curl_easy_perform(curl);
		if (res != CURLE_OK) {
			fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
		}

		// Cleanup
		curl_easy_cleanup(curl);
	}

	// Finish the separate processs
	return NULL;
}

// Call this function with a 3 letter code representing the type of timestamp
void log_time(char *code) {
	// Declare a var for the id
	pthread_t id;

	pthread_create(&id, NULL, _log_time, code);
}

