import click
from github import Github


@click.command('list-remote')
@click.pass_context
def list_remote_command(ctx: click.Context):
    """List all remote repositories."""

    github: Github = ctx.obj['github']

    for repo in github.get_user().get_repos():
        click.echo(repo.full_name)
