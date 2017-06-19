# kingkong-godzilla
King Kong versus Godzilla. A twitter competition carried out during SATToSE 17.

Participants were divided into two teams: KingKong and Godzilla. Tweets posted during the workshop using #SATToSE17 hashtag were considered for the competition.

The scores of the teams were calculated as follows: for each tweet of the team we add 1 point + its number of favs + its number of retweets. The total sum is then multiplied by a corrector. The corrector is equal to 1 if all the team members have tweeted at least once using #SATToSE17; and it is lesser than 1 otherwise.

- tweets.csv stores the tweets generated during the workshop. The file contains tweet id, number of favs, number of retweets and user name for each tweet. 
- counterhashtag.py is the Python script that generates the scores of the teams.
