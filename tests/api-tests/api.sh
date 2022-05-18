#!/bin/sh

# Exit on error, reference https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -euo pipefail

URL="http://localhost:8000"

# TODO: /root must be ok
http GET $URL

# TODO: /reports must output a list of reports with their status
http GET $URL

# TODO: /report/submit must let us submit a new report for processing
#   accepted formats are JSON and CSV, anything else should result in an error
http PUT $URL

# TODO: Accessing specific report before it is ready should result in an error
http GET $URL
