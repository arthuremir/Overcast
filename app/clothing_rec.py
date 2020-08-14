def temp_rec(temp):
    rec = ''

    if temp < -30:
        rec += 'Wait, what?'
    elif -30 <= temp < -20:
        rec += 'Put on at least 3 sweaters!'
    elif -20 <= temp < -10:
        rec += 'Put on a sweater and your warmest jacket!'
    elif -10 <= temp < 0:
        rec += 'Put on a sweater and a jacket!'
    elif 0 <= temp < 7:
        rec += 'Sweater weather!'
    elif 7 <= temp < 18:
        rec += 'Put on a jacket!'
    elif 18 <= temp < 30:
        rec += 'No outerwear needed!'
    elif 30 <= temp < 40:
        rec += 'It\'s too warm! Take a fan with you!'
    elif 40 <= temp:
        rec += 'Stay home and use a fan!'

    return rec


def condition_rec(conditions_list):
    rec = ''
    if 'Thunderstorm' in conditions_list:
        rec += 'There will be a storm. Be careful!'
    elif 'Rain' in conditions_list or 'Drizzle' in conditions_list:
        rec += 'Don\'t forget an umbrella!'

    return rec
