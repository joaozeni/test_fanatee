#! /usr/bin/env python3

import click
import requests


@click.group()
def cli():
    pass

@click.command()
@click.argument('file_path')
def insert(file_path):
    """
    FILE_PATH is the path to the csv map.
    """
    try:
        data = {'map': open(file_path, 'rb')}
    except:
        click.echo('Arquivo não pode ser aberto')
        return

    response = requests.post("http://localhost:5000/paths/insert_map", files=data)
    if response.status_code == 201:
        click.echo('inserido')
    elif response.get_json('message') == 'NO_FILE':
        click.echo('Arquivo inexistente')
    elif response.get_json('message') == 'WRONG_FORMAT':
        click.echo('Arquivo no formato errado')

@click.command()
def search():
    """
    Run the command and you can pass route in the format [ORIGIN]-[DESTINY] or type exit to leave.
    """
    while True:
        value = click.prompt('Please enter the route or enter exit to leave: ')
        if value == 'exit':
            click.echo('goodbye')
            return
        values = value.split('-')
        if len(values) != 2:
            click.echo('route inserted in wrong format')
        response = requests.get(f'http://localhost:5000/paths/search_path?origin={values[0]}&destiny={values[1]}')
        if response.status_code == 204:
            click.echo(f'no path found between {values[0]} and {values[1]}')
        path = ''
        for point in response.json().get('path'):
            path = path + point + ' - '

        path = path[:len(path)-3]
        cost = response.json().get('cost')
        click.echo(f'best route: {path} > {cost}')

cli.add_command(insert)
cli.add_command(search)

if __name__ == '__main__':
    cli()

