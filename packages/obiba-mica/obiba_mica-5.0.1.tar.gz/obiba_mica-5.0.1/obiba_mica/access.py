"""
Mica permissions
"""

import obiba_mica.core as core

SUBJECT_TYPES = ('USER', 'GROUP')

def add_permission_arguments(parser, fileArg):
  """
  Add permission arguments
  """
  parser.add_argument('--add', '-a', action='store_true', help='Grant an access right')
  parser.add_argument('--delete', '-d', action='store_true', required=False, help='Delete an access right')
  if fileArg:
    parser.add_argument('--no-file', '-nf', action='store_true', help='Do not apply the access to the associated files')
  parser.add_argument('--subject', '-s', required=True, help='Subject name to which the access will be granted. Use wildcard * to specify anyone or any group')
  parser.add_argument('--type', '-ty', required=False, help='Subject type: user or group')

def validate_args(args):
  """
  Validate action, permission and subject type
  """
  if not args.add and not args.delete:
    raise Exception("You must specify an access operation: [--add|-a] or [--delete|-de]")

  if not args.type or args.type.upper() not in SUBJECT_TYPES:
    raise Exception("Valid subject types are: %s" % ', '.join(SUBJECT_TYPES).lower())

def do_ws(args, path):
  """
  Build the web service resource path
  """
  file = 'true'
  if 'no_file' in args and args.no_file:
    file = 'false'
  if args.add:
    return core.UriBuilder(path) \
      .query('type', args.type.upper()) \
      .query('principal', args.subject) \
      .query('file', file) \
      .build()

  if args.delete:
    return core.UriBuilder(path) \
      .query('type', args.type.upper()) \
      .query('principal', args.subject) \
      .build()
