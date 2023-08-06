
import os, yaml, sys
from src.utils.context import Context
from src.utils.chalk import chalk
from src.utils.utils import run_hooks


Context.root_path = os.getcwd()
Context.config_file_path = os.path.join(Context.root_path, 'pyclk.yaml')
Context.commands = getattr(sys.modules['src'], 'commands')

#########################
#                       #
#   @pending changes    #
#   load version        #
#                       #
#########################
try:
  ###################
  #                 #
  #   production    #
  #                 #
  ###################
  from version import __version__ as version
  Context.version = version
except Exception as e:
  ###################
  #                 #
  #   development   #
  #                 #
  ###################
  with open("reqs.yaml", "r") as f:
    Context.version = yaml.safe_load(f)["version"]

def read_config():
  try:
    with open(Context.config_file_path, 'r') as stream:
      Context.config = yaml.safe_load(stream)
  except:
    print("Error: Could not load config file.")

def read_args():
  command_and_args = []
  flags = []

  def _get_flags(v: str):
    return v.__contains__('-') or v.__contains__('--')

  for arg in sys.argv:
    if _get_flags(arg):
      flags.append(
        arg.split('--')[1] if arg.__contains__('--') 
        else arg.split('-')[1]
      )
    else:
      command_and_args.append(arg)
  
  Context.command['flags'] = flags
  
  if len(command_and_args) == 1:
    return (None, None)
  try:
    return (command_and_args[1], command_and_args[2])
  except:
    return (command_and_args[1], None)

def run_command(cmd, args):
  try:
    status = Context.get_command(cmd)()
    ###################
    #                 #
    #    Run hooks    #
    #                 #
    ###################
    run_hooks(cmd) if status else None
    Context.flush_flags()
  except Exception as e:
    chalk.red("Error: Command not found")

def main():
  """
    Execute validation checks,
    and parse config files
  """
  read_config()
  (command, project) = read_args()
  if command is None:
    chalk.green(f"PyCLK v{Context.version}")
    sys.exit(0)

  Context.command['args'] = project
  Context.command['command'] = command

  run_command(command, project)
