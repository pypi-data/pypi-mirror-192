import os
import json
from pathlib import Path

import click
from github import Github
from gitflux import __version__
from gitflux.commands import list_repos_command, create_repos_command, delete_repos_command, sync_repos_command

__config_file__ = Path(Path.home(), '.gitflux', 'config.json')


def print_version(ctx: click.Context, _, value: bool):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


def init(ctx: click.Context, _, value: bool):
    if not value or ctx.resilient_parsing:
        return

    os.makedirs(os.path.dirname(__config_file__), 0o700, exist_ok=True)

    with open(__config_file__, 'w', encoding='utf-8') as fp:
        json.dump({
            'github': {
                'accessToken': click.prompt('GitHub access token', type=str)
            }
        }, fp, indent=4, ensure_ascii=False)

    os.chmod(__config_file__, 0o600)
    ctx.exit()


@click.group()
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('--init', help='Initialize configurations.', is_flag=True, callback=init, expose_value=False, is_eager=True)
@click.pass_context
def cli(ctx: click.Context):
    """A command-line utility to help you manage repositories hosted on GitHub."""

    ctx.ensure_object(dict)

    with open(__config_file__, 'r', encoding='utf-8') as fp:
        config = json.load(fp)

    ctx.obj['github'] = Github(login_or_token=config['github']['accessToken'])


cli.add_command(list_repos_command)
cli.add_command(create_repos_command)
cli.add_command(delete_repos_command)
cli.add_command(sync_repos_command)

if __name__ == '__main__':
    cli(obj={})  # pylint: disable=no-value-for-parameter
