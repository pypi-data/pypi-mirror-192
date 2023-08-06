import importlib.metadata
from pathlib import Path

__version__ = importlib.metadata.version('git_timemachine')

__config_file__ = Path(Path.home(), '.git-timemachine', 'config')
