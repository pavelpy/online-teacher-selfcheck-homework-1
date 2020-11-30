"""Обработка файла и конвертирование его в файл `criteria-list.js`"""
from collections import defaultdict, namedtuple
from pprint import pprint
from string import Template
import json
import re

try:
    import markdown2
except ImportError:
    class markdown2:
        @staticmethod
        def markdown(in_text):
            return in_text

CheckInfo = namedtuple('CheckInfo', 'check_item, requirements_title, requirements_type')

PRIMARY_AND_ADDITIONAL_REQUIREMENTS_LIST = (
    CheckInfo('#### Основные требования', 'Основные требования', 'main'),
    CheckInfo('#### Дополнительные требования', 'Дополнительные требования', ''),
)

CRITERIA_LIST_JS_TEMPLATE = Template("""export const GOOD_TOTAL_POINTS = $max_total_points;
export const MINIMAL_TOTAL_POINTS = 40;
export const criteria = $json_dict;""")

URL_REGEX = r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"


def make_html_link(text):
    result = re.sub(URL_REGEX, r'<a href="\1" target="_blank">\1</a>', text, flags=re.MULTILINE)
    return result


def get_first_match(in_str, check_and_return_list):
    for check_item, requirements_title, requirements_type in check_and_return_list:
        if in_str.startswith(check_item):
            return (requirements_title, requirements_type)
    return None


def main():
    # TODO: поменять split на regex для ухудшения читаемости?) <Pavel 2020-03-16>
    file_content = open('./criteria_list.md').read()
    requirements_type = 'main'
    requirements = list()
    id_counter = 0
    max_total_points = 0
    for line in file_content.splitlines(False):
        first_match = get_first_match(line, PRIMARY_AND_ADDITIONAL_REQUIREMENTS_LIST)
        if first_match:
            requirements_title, requirements_type = first_match
            vals = {'type': "title", 'title': requirements_title}
            requirements.append(vals)
        elif line.startswith('* '):
            line = line[2:]
            text, mod = line.rsplit(' (', 1)
            mod = int(mod.split(' ', 1)[0])
            vals = {
                'id': id_counter,
                'text': make_html_link(text),
                'mod': mod,
                'i': '',
            }
            max_total_points += mod
            # if requirements_type == 'main':
            #     vals['status'] = 'main'

            requirements.append(vals)
            id_counter += 1

    json_dict = json.dumps(requirements, ensure_ascii=False, indent=2)
    file_content = CRITERIA_LIST_JS_TEMPLATE.substitute(
        {'json_dict': json_dict,
         'max_total_points': max_total_points,
         })
    with open('./criteria-list.js', 'w') as f:

        f.write(file_content)
    # print(file_content)


if __name__ == '__main__':
    main()
