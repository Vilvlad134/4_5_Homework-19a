
#######################################Задание-2#################################################

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


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        div(4, 2)
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()