# WIP: Python NBA Data Pipeline

## Steps:
1. install mysql
2. set up username and password
3. mysql server start
4. mysql -u <USER_NAME> -p
5. type in password
6. create database nba_data;
7. create creds file in form of (see MySqlCredExample.json):
```
{
  "Username": <USER_NAME>,
  "Password": <PASSWORD>
}
```
8. install Anaconda: https://www.anaconda.com/distribution/
9. conda env create


## Commands

#### Download Game Log
`python3 -m src.etl.game_log -h`

#### Download Box Scores
`python3 -m src.etl.box_score_traditional -h`

#### Download Tracking Data
`python3 -m src.etl.player_tracking_season_totals -h`