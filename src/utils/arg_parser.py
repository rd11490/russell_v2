def season_arg(parser):
    parser.add_argument('-s', '--season', action="store", dest='season', help='The season you are trying to download')


def season_type_arg(parser):
    parser.add_argument('-st', '--season_type', action="store", dest='season_type',
                        help='The season type you are trying to download')


def game_id_arg(parser):
    parser.add_argument('-g', '--game_id', action="store", dest='game_id',
                        help='The game id of the game you are trying to download')


def player_id_arg(parser):
    parser.add_argument('-p', '--player_id', action="store", dest='player_id',
                        help='The player id of the player you are trying to download')


def team_id_arg(parser):
    parser.add_argument('-tm', '--team_id', action="store", dest='team_id',
                        help='The team id of the team you are trying to download')


def run_all_arg(parser):
    parser.add_argument('-ra', '--run-all', action='store_true', dest='run_all', help='Run All Commands')


def force_arg(parser):
    parser.add_argument('-f', '--force', action='store_true', dest='force', help='Force Command')


def delta_arg(parser):
    parser.add_argument('-d', '--delta', action='store_true', dest='delta', help='Delta Command')
