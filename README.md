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


## Commands

#### Download Game Log
`python3 -m src.etl.game_log -s 2018-19 -st 'Regular Season'`

#### Download Box Scores
`python3 -m src.etl.box_score_traditional -s 2018-19 -st 'Regular Season'`