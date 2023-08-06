import os
from datetime import datetime

import click
from git_timemachine import __version__, __config_file__
from git_timemachine.config import Config
from git_timemachine.commands import log_command, commit_command, grow_command, migrate_command


def print_version(ctx: click.Context, _, value: bool):  # pragma: no cover
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


def init(ctx: click.Context, _, value: bool):
    if not value or ctx.resilient_parsing:
        return

    profile_dir = os.path.dirname(__config_file__)
    os.makedirs(profile_dir, 0o700, exist_ok=True)

    Config(__config_file__, data={
        'commit': {
            'start-hour': 19,
            'growth-range': '600-3600'
        },
        'states': {
            'last-committed': datetime.now().replace(microsecond=0).astimezone().isoformat()
        }
    }).write()

    ctx.exit()


@click.group()
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('--init', help='Initialize git-timemachine.', is_flag=True, callback=init, expose_value=False)
@click.pass_context
def cli(ctx: click.Context):
    """A command-line tool to help you manage Git commits at different time nodes."""

    ctx.ensure_object(dict)
    ctx.obj['config'] = Config(__config_file__)
    ctx.obj['config'].read()


cli.add_command(log_command)
cli.add_command(commit_command)
cli.add_command(grow_command)
cli.add_command(migrate_command)

if __name__ == '__main__':
    cli()
