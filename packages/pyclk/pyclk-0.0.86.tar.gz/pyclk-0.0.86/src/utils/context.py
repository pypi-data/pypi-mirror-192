class _ServiceContext:
  def __init__(self):
    self.config = {}
    self.root_path = ""
    self.config_file_path = ""
    self.command = {
      'args': [],
      'command': '',
      'flags': [],
    }
    self.project = {}
    self.args = {}
    self.commands = {}
    self.version = ""

  def get_command(self, cmd):
    _to_run = (
      'help' 
        if ('help' or 'h') in self.command['flags']
        else cmd
      )
    return getattr(
      getattr((self.commands), cmd),
    _to_run)
  
  def flush_flags(self):
    self.command['flags'] = []

Context = _ServiceContext()