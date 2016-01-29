#This Readme covers what each file means

##contents of crontab

This file contains the cronjobs that are being done on an hourly bases.

##copy.sh

This file is in the cronjobs, it periodically every hour collects all the tweets
with the search criteria AAPL and just prints them out. The output of this file
is fed into a JSON file periodically.

##JSON_DB.py

This file takes the contents of the saved JSON files from copy.sh and puts them 
into a database that is used for this project.

##AAPL.json

This is a set of all the tweets that we considered for this project. It can be 
added to a mongodb using the command

mongoimport -d tweets -c RawTweets database.json

That will set it up for the code that we have used.

##AAPL_learn.py

This is the final project code that reads from the db and does all the learing
and all.