import os
from ..utils.context import Context
from ..utils.logger import loading_process, completed_process, show_help

def purge():
  r = Context.root_path
  loading_process(
    f"Purging packages at: {r}",
    os.system,
    args=[f"rm -rf {r}/python_modules"]
  )
  completed_process("\nPackages purged successfully")
  
def help():
  show_help(
    command='purge',
    description='Purges all python packages in your project',
    usage=[
      {
        'command': 'purge',
        'description': 'Removes all python packages in your project (using your virtual environment)'
      }
    ]
  )