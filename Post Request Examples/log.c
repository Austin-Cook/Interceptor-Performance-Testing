#include <curl/curl.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>
#include <time.h>

// Struct to hold args used in helper method
struct arg_struct {
	char *code;
	struct timeval now;
};

// Helper method
static void *_log_time(void *args_ptr) {
	CURL *curl;
	CURLcode res;

	// Get the args
	struct arg_struct *args = (struct arg_struct *)args_ptr;
	char *identifier = args->code;
	struct timeval now = args->now;

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
	}

	// Cleanup
	free(args->code);
	free(args);
	if (curl) {
		curl_easy_cleanup(curl);
	}

	// Finish the separate processs
	return NULL;
}

void log_time(char *code) {
	// Declare a var for the id
	pthread_t id;

	// Allocate memory for arg_struct
	struct arg_struct *args = (struct arg_struct *)malloc(sizeof(struct arg_struct));
	if (args == NULL) {
		printf("Error - log.c: Failed to allocate memory for arg_struct struct\n");
		exit(1);
	}

	// Allocate memory for the code
	args->code = (char *)malloc(4 * sizeof(char));
	if (args->code == NULL) {
		printf("Error - log.c: Failed to allocate memory for code\n");
		free(args->code);
		exit(1);
	}

	// Fill the struct
	strcpy(args->code, code);
	gettimeofday(&args->now, NULL);

	pthread_create(&id, NULL, _log_time, (void *)args);
}

