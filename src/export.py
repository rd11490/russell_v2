from src.utils.client import *

out = smart.get_shot_chart_detail(player_id='201939',team_id='1610612744', season='2018-19', season_type='Regular Season')
print(out)

print(out.columns)