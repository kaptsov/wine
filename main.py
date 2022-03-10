from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from collections import defaultdict

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

foundation_date = datetime.date(year=1920, month=1, day=1)
delta = (datetime.date.today() - foundation_date).days // 365


excel_data_df2 = pandas.read_excel(
    'wine3.xlsx',
    sheet_name='Лист1',
    na_values=['N/A', 'NA'],
    keep_default_na=False
)

wine_data = excel_data_df2.to_dict(orient='record')

drink_types = defaultdict(list)

for drink in wine_data:
    drink_types[drink['Категория']].append({
        'name': drink['Название'],
        'price': drink['Цена'],
        'type': drink['Сорт'],
        'pic_name': drink['Картинка'],
        'sale': drink['Акция'],
    })

rendered_page = template.render(
    age=delta,
    wine_data=dict(sorted(drink_types.items())),
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
