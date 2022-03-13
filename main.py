import argparse
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

FOUNDATION_DATE = 1920


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='+')
    return parser


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    current_year = datetime.date.today().year

    parser = create_parser()
    excel_filename = str(parser.parse_args().filename[0])

    wine_collection = pandas.read_excel(
        excel_filename,
        sheet_name='Лист1',
        na_values=['N/A', 'NA'],
        keep_default_na=False
    ).to_dict(orient='record')

    drink_description = defaultdict(list)

    for drink in wine_collection:
        drink_description[drink['Категория']].append({
            'Название': drink['Название'],
            'Цена': drink['Цена'],
            'Сорт': drink['Сорт'],
            'Картинка': drink['Картинка'],
            'Акция': drink['Акция'],
        })

    rendered_page = template.render(
        age=current_year - FOUNDATION_DATE,
        drink_description=dict(sorted(drink_description.items())),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
