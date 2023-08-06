import os
import click


@click.command('sync-repos')
@click.argument('base_path', type=click.Path(file_okay=False), default=os.getcwd())
@click.option('-b', '--branch', type=str, default='main', help='Branch to synchronize with')
def sync_repos_command(base_path: str, branch: str):
    """Synchronize repositories with remote."""

    cwd = os.getcwd()

    for file in os.listdir(base_path):
        repos_dir = os.path.join(base_path, file)

        if os.path.isfile(repos_dir):
            continue

        os.chdir(repos_dir)

        if 'nothing to commit, working tree clean' in str(os.popen('git status').read()):
            click.echo(f'Synchronizing repository: {file}...')
            os.system(f'git pull origin {branch}')
            os.system(f'git push origin {branch}')
            click.echo()
        else:
            click.echo(f'WARNING: Repository "{repos_dir}" not clean.', err=True)

    os.chdir(cwd)
