import codecs
from datetime import datetime
import pandas as pd


def get_xyuno_data(file_path: str) -> list:
    file_obj = codecs.open(file_path, "r", "utf_8_sig")
    result = [line.replace('\n', '').replace('\r', '') for line in file_obj.readlines()]  # straight to list
    file_obj.close()
    # print(result)
    return result


def process_xyuno_data_and_get_lol_struct(log_lines, st_xyuno_tab):
    # separate events by dates
    events = []
    temp_arr = []
    need_add = False
    i = 0
    while i < len(log_lines):
        line = log_lines[i]
        if line == '':
            events.append(temp_arr)
            temp_arr = []
            need_add = False
        elif line[0] == '#':
            temp_arr.append(log_lines[i])
            need_add = True
        elif need_add:
            temp_arr.append(log_lines[i])
        i += 1
    # print(events)

    # add col names
    result_lol_tab = [list(st_xyuno_tab.keys())]
    for i, event in enumerate(events):
        event_id = i + 1
        games_per_event = [s for s in event[1].split(' ') if s.isdigit()]
        games_qty = len(games_per_event)
        for n in range(games_qty):
            for line in event:
                if '#' in line:
                    process_type = 'date_place'
                    date_place = process_line(line[1:], process_type)
                    date, place = date_place
                else:
                    process_type = 'plr_res'
                    game_id = n + 1
                    pl_res_per_evnt = process_line(line, process_type)
                    # check diff names and make unique for 1 pers
                    name = unify_name(pl_res_per_evnt.pop(0))
                    result = pl_res_per_evnt[n]
                    if result == '-':
                        continue
                    new_line = {}
                    new_line.update(st_xyuno_tab)
                    new_line['Event_id'] = event_id
                    new_line['Game_id'] = game_id
                    new_line['Player'] = name
                    new_line['Result'] = result
                    new_line['Place'] = place
                    new_line['Date'] = unify_date_format(date)
                    result_lol_tab.append(list(new_line.values()))
    print(len(result_lol_tab))
    return result_lol_tab


def process_line(line: str, process_type) -> list:
    arr = line.split(' ')
    if process_type == 'plr_res':
        name = arr.pop(0)
        i = 0
        while not arr[i].isdigit():
            if arr[i] != '-':
                name += f' {arr.pop(i)}'
                i += 1
            else:
                break
        arr.insert(0, name)
    elif process_type == 'date_place':
        i = 1
        place = ''
        while i < len(arr):
            place += f'{arr.pop(i)} '
            if len(arr) == 1:  # to skip `else`
                place = place[:-1]  # get rid of ' '
                break
        else:
            place = 'Unknown'
        arr.append(place)
    return arr


def is_date(string, fuzzy=False) -> bool:
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    from dateutil.parser import parse
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def unify_date_format(strdate: str) -> str:
    """
    Transform date from 01.02.2020 -> 01.02.20
    :param strdate: date after `#`
    :return: date in format `dd.mm.yy`
    """
    if len(strdate) == 10:
        result = datetime.strptime(strdate, '%d.%m.%Y').strftime('%d.%m.%y')
    else:
        result = strdate
    return result


def unify_name(name: str) -> str:
    if name == 'Я':
        result = 'Кичик'
    elif name in ['Лешик', 'Лёша', 'Клачковский', 'Ленин']:
        result = 'Клачков'
    elif name in ['Сас', 'Стасян']:
        result = 'Стас'
    elif name == 'Владушкин':
        result = 'Влад'
    else:
        result = name
    return result


def save_to_excel(lol, file_path, save=False) -> None:
    if save:
        pd.DataFrame(lol).to_excel(file_path, header=False, index=False)


if __name__ == '__main__':
    print(get_xyuno_data('../Data/xyuno_Log.txt'))
