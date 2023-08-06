import os,yaml, sys
from ..utils.dumper import PrettyDumper
from ..utils.context import Context
from ..utils.logger import completed_process, loading_process, failed_process, show_help
from spinners import Spinners
from threading import Thread
import subprocess
from typing import List


def _remove_packages_conflicts(current: List[str], new: List[str]) -> List[str]:
  """
    Removes packages that are already installed.
  """
  combined_list = current + new
  unique_packages = {}
  for package in combined_list:
      package_parts = package.split('==')
      package_name = package_parts[0]
      if package_name not in unique_packages:
          unique_packages[package_name] = package_parts[1]
  return [f'{package}=={version}' for package, version in unique_packages.items()]

def _remove_empty(v):
  return True if len(v) > 0 else False

def _add_to_state():
  """
    Reads reqs.yaml and adds the new package to 
    the reqs.packages list.
  """

  root_path = Context.root_path
  activate_script = os.path.join(root_path, "python_modules", "bin", "activate")
  with open(os.path.join(root_path,'reqs.yaml'), 'r') as stream:
    Context.project = yaml.safe_load(stream)
  output = subprocess.check_output(f"/bin/bash -c \"source {activate_script} && pip freeze\"", shell=True).decode('utf-8')
  packages = list(filter(_remove_empty, output.split('\n')))
  Context.project['packages'] = _remove_packages_conflicts(Context.project['packages'], packages)

  with open(os.path.join(root_path,'reqs.yaml'), 'w') as stream:
    yaml.dump(
      Context.project,
      stream,
      default_flow_style=False,
      sort_keys=False,
      indent=2,
      Dumper=PrettyDumper
    )

def install():
  root_path = Context.root_path
  with open(os.path.join(root_path, 'reqs.yaml'), 'r') as stream:
    Context.project = yaml.safe_load(stream)

  packages_list = (
    " ".join(Context.project['packages']) if Context.command['args'] is None
    else Context.command['args']
  )
  if not os.path.isdir(os.path.join(root_path, 'python_modules')):
    print("Creating python_modules folder...")
    state = os.system(f'cd {root_path}\npython3 -m venv python_modules')
    if state != 0:
      failed_process("[Error]: Failed to create python_modules folder")
      os.system(f"rm -rf {root_path}/python_modules 2> /dev/null")
      return False
    
  path_to_python_version = os.path.join(
    root_path,
    "python_modules",
    "lib"
  )
  python_version = os.listdir(path_to_python_version)[0]
  path_to_env_folder = os.path.join(
    root_path,
    "python_modules",
    "lib",
    python_version,
    "site-packages"
  )

  loading_process(
    log=(
      "Installing full project..." if Context.command['args'] is None
      else f"Installing {packages_list}..."
    ),
    f=os.system,
    args=[f"pip install --quiet {packages_list} --target {path_to_env_folder} --upgrade"]
  )
  
  _add_to_state() if Context.command['args'] is not None else None
  
  completed_process("\nProject installed successfully")
  return True


def help():
  show_help(
    command='install',
    description='Installs packages into the python_modules folder',
    usage=[
      {
        'command': 'install',
        'description': 'Installs packages into the python_modules folder'
      },
      {
        'command': 'install <packages>',
        'description': 'Installs specific packages only'
      }
    ]
  )
  