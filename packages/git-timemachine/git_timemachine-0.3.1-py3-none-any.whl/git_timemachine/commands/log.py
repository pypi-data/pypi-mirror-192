import json
import os

import click
from git_timemachine.repo import get_commit_logs


@click.command('log')
@click.argument('repo_dir', type=click.Path(exists=True, file_okay=False), default=os.getcwd())
def log_command(repo_dir: str):
    """Show logs of Git repository commits."""

    click.echo(json.dumps(get_commit_logs(repo_dir), ensure_ascii=False, indent=4))
