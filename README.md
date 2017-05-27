# python script to post lms squeezebox info to mqtt
Connects to lms server to gather info for individual players and posts this
info to mqtt server for other subscribed clients
refreshes every minute from lms telnet session and posts changes to mqtt
