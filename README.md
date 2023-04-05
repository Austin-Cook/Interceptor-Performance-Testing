# Interceptor Performance Testing
Contains a set of tools to measure the time to perform operations in microseconds.

## Files
- *Report Server*
  - A simple HTTP server to receive the timestamps
  - Enables integration of timestamps from multiple independent programs
- *Post Request Examples*
  - Code to print a timestamp in C and Python
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
