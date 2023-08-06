from datetime import datetime, timedelta

import click


@click.command('grow')
@click.pass_context
def grow_command(ctx):
    """Grow date time of last committed."""
    config = ctx.obj['config']

    dt = datetime.fromisoformat(config.get('states', 'last-committed')) + timedelta(hours=24)

    config.set('states', 'last-committed', dt.replace(hour=int(config.get('commit', 'start-hour')), minute=0, second=0, microsecond=0).astimezone().isoformat())
    config.write()
