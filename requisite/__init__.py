import sys
from pip import autocomplete, version_control
from pip.baseparser import parser
from pip.basecommand import command_dict

def main(initial_args=None):
  if initial_args is None:
    initial_args = sys.argv[1:]
  autocomplete()
  version_control()
  options, args = parser.parse_args(initial_args)
  if options.help and not args:
    args = ['help']
  if not args:
    parser.error('You must give a command?')
  cmd = 'requisite'
  fn = 'requisite.commands.%s' % cmd
  try:
    __import__(fn)
  except ImportError:
    pass
  
  command = command_dict[cmd]
  return command.main(initial_args, args, options)
