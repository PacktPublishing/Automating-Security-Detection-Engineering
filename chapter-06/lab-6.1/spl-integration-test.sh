#!/bin/bash

### ENTER IN TERMINAL ###
# Ensure splunk is running sudo /opt/splunk/bin/splunk start
# you will need to sudo your exports because of session swap
# in a CI this is easier to run as root because of env variable injections
# run sudo bash
# export SPLUNK_USER='<your login>'
# export SPLUNK_PASSWORD='<your password>'

### buildspec.txt format ###
#TEST_LOG:/tmp/audit-example-log.txt
#SPL_SEARCH:index=main jsmith

#SPL_USER=$(env | grep SPLUNK_USER | cut -d '=' -f2)
#SPL_PASSWORD=$(env | grep SPLUNK_PASSWORD | cut -d '=' -f2)
SPL_LOG="$pwd$(cat ./buildspec.txt | grep TEST_LOG | cut -d ':' -f2)"
SPL_SEARCH=$(cat ./buildspec.txt | grep SPL_SEARCH | cut -d ':' -f2)

echo $SPL_LOG
#echo "$SPLUNK_USER:$SPLUNK_PASSWORD"
echo $SPL_SEARCH

echo "Adding test log entry..."

sudo /opt/splunk/bin/splunk add oneshot $SPL_LOG -index main -hostname 127.0.0.1 -sourcetype 'syslog:linux:auditd' -auth "$SPLUNK_USER:$SPLUNK_PASSWORD"

echo "Waiting for indexing..."
sleep 3
echo "Testing search..."

RESULTS=$(sudo /opt/splunk/bin/splunk search "$SPL_SEARCH" -app search -maxout 10 -output auto -timeout 120 | wc -l)

echo "Found: $RESULTS"

if [[ $RESULTS -gt 0 ]]; then
	echo "Test PASS."
else
	echo "Test FAILED."
	sudo /opt/splunk/bin/splunk stop
	sudo /opt/splunk/bin/splunk clean eventdata -index main -f
	echo "restarting splunkd for future testing..."
	sudo /opt/splunk/bin/splunk start
	exit 1
fi

echo "cleaning up logs from index..."
sleep 1
echo "splunkd must stop before cleaning.."
sudo /opt/splunk/bin/splunk stop
sudo /opt/splunk/bin/splunk clean eventdata -index main -f
echo "restarting splunkd for future tests..."
sudo /opt/splunk/bin/splunk start
exit 0