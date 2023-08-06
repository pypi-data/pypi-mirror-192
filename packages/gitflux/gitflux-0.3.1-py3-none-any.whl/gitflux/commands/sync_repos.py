import os
import click
from github import Github


@click.command('sync-repos')
@click.argument('base_path', type=click.Path(file_okay=False), default=os.getcwd())
@click.option('--branch', type=str, default='main', help='Branch to synchronize with')
@click.option('--auto-create', is_flag=True, help='Auto-create remote repositories')
@click.option('--user', type=str, default=None, help='GitHub user to create remote repositories')
@click.option('--private', help='Private repository.', is_flag=True, default=True)
@click.pass_context
def sync_repos_command(ctx: click.Context, **kwargs):
    """Synchronize repositories with remote."""

    github: Github = ctx.obj['github']
    repos = github.get_user().get_repos()

    owner = github.get_user()

    if (kwargs['user'] is not None) and (kwargs['user'] != owner.login):
        owner = github.get_organization(kwargs['user'])

    cwd = os.getcwd()

    for file in os.listdir(kwargs['base_path']):
        repos_dir = os.path.join(kwargs['base_path'], file)

        if os.path.isfile(repos_dir):
            continue

        new_repo = False

        if kwargs['auto_create'] and next((x for x in repos if x.full_name == f'{owner.login}/{file}'), None) is None:
            click.echo(click.style(f'[gitflux] Creating remote repository: {file}', fg='green'))
            owner.create_repo(file, private=kwargs['private'])
            new_repo = True

        if os.path.isfile(repos_dir):
            continue

        os.chdir(repos_dir)

        if 'nothing to commit, working tree clean' in str(os.popen('git status').read()):
            click.echo(click.style(f'[gitflux] Synchronizing repository: {file}', fg='green'))

            if not new_repo:
                os.system(f'git pull origin {kwargs["branch"]}')

            os.system(f'git push origin {kwargs["branch"]}')
        else:
            click.echo(click.style(f'[gitflux] Repository "{repos_dir}" not clean.', fg='red'), err=True)

        click.echo()

    os.chdir(cwd)
