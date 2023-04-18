# Interceptor Performance Testing
Contains a set of tools to measure the time to perform operations in microseconds.

## Folders
- *Report Server*
  - A simple HTTP server to receive the timestamps
  - Enables integration of timestamps from multiple independent programs
- *POST Timestamp*
  - Code to submit a timestamp to the server from either C or Python
    - For C, put log.h and log.c in your code and follow the note at the bottom of this page to make libcurl available to log.c
    - For python, put log.py in your code and include log_time function in the file where timestamps will be collected
- *ctime-binding*
  - A binding to allow receiving time in Python using the C sys/time.h gettimeofday() function
  - Must install to your system following the instructions in the README in the folder
- *Timestamp Analysis*
  - A set of tools for analyzing timestamps from the server
  - analysis.py
    - Contains analysis methods for specific metrics
  - report_log.txt
    - Must copy the log from the report server here to be read for analysis
  - timestamp.py
    - Represents a single Timestamp object
  - timestamp_util.py
    - Contains helpful utilities for reading logs and processing timestamps

## Note
- To link libcurl to the executables add these to the CMakeLists.txt file in interceptor-libevdev/src or equivalent folder
  - Add `find_package(CURL REQUIRED)` to the find_package statements
  - Create and new library for the performance testing files and link libcurl to it
    - `add_library(performance_testing OBJECT log.c)`
    - `target_link_libraries(performance_testing PUBLIC CURL::libcurl)`
  - Link the new library to all libraries that where the logger will be used
    - `target_link_libraries(library_name performance_testing)`
