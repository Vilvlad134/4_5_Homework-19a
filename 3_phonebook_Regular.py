
#######################################Задание-3#################################################

import re
import csv
from pprint import pprint
import os
import logging


def logger(path):

    def _logger(old_function):

        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            logging.basicConfig(level=logging.INFO, filename=path, filemode="w", force=True,
                                format="%(asctime)s %(levelname)s %(message)s")
            logging.info(f"вызвана функция {old_function.__name__} с аргументами {args}{kwargs} и результатом {result}")

            return result

        return new_function

    return _logger


# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


@logger('log1.log')
def index_sorting_phoneformat():
    # распределяем значения по своим индексам
    for li in contacts_list[1:]:
        line = li[0] + ' ' + li[1] + ' ' + li[2]
        pattern_obj = (r'\w+')
        result = re.findall(pattern_obj, line)
        for it in result:
            li[result.index(it)] = it

    # приводим телефоны в нужный формат
        pattern_obj = re.compile(
            r"(\+7|8)(\s*)?(\()?(\d{3})(\))?(\s*|-)?(\d{3})([-\s]+)?(\d{2})([-\s]+)?(\d{2})((\s*)?(\()?((доб.) (\d+))(\))?)?")
        # for lists in contacts_list[1:]:
        li[5] = pattern_obj.sub(r"+7(\4)\7-\9-\11 \16\17", li[5])


@logger('log2.log')
def data_aggregation():
    # объединяем данные повторяющихся пользователей
    k = 0
    while k < len(contacts_list) - 1:
        for lk in contacts_list:
            if contacts_list[k][0] == lk[0] and contacts_list[k][1] == lk[1] and contacts_list[k] != contacts_list[contacts_list.index(lk)]:
                new_list = [list1 or list2 for list1, list2 in zip(contacts_list[k], contacts_list[contacts_list.index(lk)])]
                contacts_list[k] = new_list
                contacts_list.remove(contacts_list[contacts_list.index(lk)])
        k += 1


@logger('log3.log')
def data_recording():
    # код для записи файла в формате CSV
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)


def main():
    index_sorting_phoneformat()
    data_aggregation()
    data_recording()
    pprint(contacts_list)

if __name__ == '__main__':
    main()