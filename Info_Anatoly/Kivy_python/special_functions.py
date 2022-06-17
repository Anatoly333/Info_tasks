def clear(time, games):
    import datetime
    for id in games.keys():
        for player in games[id]['fires']:
            keys = [*games[id]['fires'][player].keys()]
            for fire in keys:
                t_f = games[id]['fires'][player][fire]['t']
                if time - t_f > 10:
                    del games[id]['fires'][player][fire]

def check_players(time, games):
    for id in [*games.keys()]:
        for player in [*games[id]['players'].keys()]:
            for fire_player in games[id]['fires']:
                # if player + 'team' not in games[id]['players'] or fire_player not in games[id]['players'][player + 'team']:
                #if fire_player != player:
                if fire_player != player:
                    for fire in games[id]['fires'][fire_player]:
                        t_f = games[id]['fires'][fire_player][fire]['t']
                        x_f = games[id]['fires'][fire_player][fire]['x']
                        y_f = games[id]['fires'][fire_player][fire]['y']
                        speed = games[id]['fires'][fire_player][fire]['speed']
                        y_now = speed * (t_f - time) + y_f
                        p = 0
                        if abs(games[id]['players'][player]['y'] - y_now) <= games[id]['players'][player]['size']:
                            p += 1
                        if abs(games[id]['players'][player]['x'] - x_f) <= games[id]['players'][player]['size']:
                            p += 1
                        if p == 2:
                            damage = games[id]['fires'][fire_player][fire]['damage']
                            games[id]['players'][player]['hp'] -= damage