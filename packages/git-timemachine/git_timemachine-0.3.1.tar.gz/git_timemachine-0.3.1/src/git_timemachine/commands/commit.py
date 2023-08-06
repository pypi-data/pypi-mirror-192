import os
import random
from datetime import datetime, timedelta

import click


@click.command('commit')
@click.option('-m', '--message', help='Message describing the changes.', required=True)
@click.argument('repo_dir', type=click.Path(exists=True, file_okay=False), default=os.getcwd())
@click.pass_context
def commit_command(ctx: click.Context, message: str, repo_dir: str):
    """Record a commit on a repository."""

    config = ctx.obj['config']

    growth = config.get('commit', 'growth-range').split('-')

    random.seed()
    dt = datetime.fromisoformat(config.get('states', 'last-committed')) + timedelta(seconds=random.randint(int(growth[0]), int(growth[1])))
    dt_str = dt.replace(microsecond=0).astimezone().isoformat()

    cwd = os.getcwd()
    os.chdir(repo_dir)

    cmd = f'git commit -m "{message}" --date {dt_str}'
    os.system(cmd)

    os.chdir(cwd)

    config.set('states', 'last-committed', dt_str)
    config.write()
