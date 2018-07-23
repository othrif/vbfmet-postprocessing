"""
  Helper classes to enable configuration of jobs
"""

"""
TODO/Note to self:
I'm pretty unsure about the whole 'parent/child' thing and how it should work with building
tools/sequences...
"""

from extended_athfile import ExtendedAthFile
from ath_argparse import AthenaArgumentParser
import logging
import argparse
logger = logging.getLogger(__name__)

class JobConfigurationValues(object):
  """Class to hold all the configuration values read from the command line, metadata, configuration files etc"""
  class ConflictPolicy:
    """Enum to describe how conflicts should be handled.
       A conflict is when the same key appears in two configuration files with different values
    """
    RAISE = 0 # Raise an exception
    TAKE_NEW = 1 # Use the new value
    KEEP_OLD = 2 # Keep the old value
    MERGE_UNIQUE = 3 # If it's a list, append the new list then call list(set(...))
    MERGE_APPEND = 4 # If it's a list, append the new list
 
  def __init__(self):
    self._configuration = {}

  @classmethod
  def merge_dicts(cls, a, b, policy=ConflictPolicy.RAISE, path=None):
    """Merge 'b' *into* 'a'. Handle conflicts according to the given policy"""
    for key, value in b.iteritems():
      new_path = key if path is None else path+"."+key
      if key in a:
        if isinstance(value, dict):
          merge_dicts(a[key], value, policy, new_path)
        elif a[key] == value:
          continue
        elif policy == ConflictPolicy.RAISE:
          raise ValueError("Error merging dictionaries. Conflict at key {0}".format(new_path) )
        elif policy == ConflictPolicy.TAKE_NEW:
          a[key] = value
        elif policy == ConflictPolicy.KEEP_OLD:
          pass
        elif policy == ConflictPolicy.MERGE_UNIQUE or policy == ConflictPolicy.MERGE_APPEND:
          try:
            a[key] += value
          except TypeError as e:
            raise ValueError("Error merging dictionaries. Conflict at key {0}".format(new_path) )
          if policy == ConflictPolicy.MERGE_UNIQUE:
            a[key] = list(set(a[key]))
      else:
        a[key] = value
    
  def _add_configuration_dict(self, new, policy=ConflictPolicy.RAISE):
    self.merge_dicts(self._configuration, new, policy)

  def config_value(self, option):
    conf = self._configuration
    try:
      for opt in option.split('.'):
        conf = conf[opt]
    except KeyError:
      raise KeyError(option)
    return conf



class JobConfigurationBase(object):
  """Class that holds all the information for configuring a job.
    Collates together information read from command line options, file metadata and anything read from
    autoconfiguration.
    Then uses this to create and configure tools and algorithms.
    Can be linked together so packages can provide their own configurations to be used by the parent job option
  """
  
  def __init__(self, title="Job Options", description="", parent=None, parser=None, metadata_reader=ExtendedAthFile, stack_depth=2):
    """
      If a parent is provided, add this to the parent. In this case, the parser argument is ignored.
      Else, create a parser if one isn't provided. Add the arguments to the parser (or the parent's).
      The metadata_reader class is used to read metadata from the input files. Only the first non-empty
      file will be used (assuming that one file's metadata will be representative).
    """

    self._metadata_reader_class = metadata_reader
    self.title = title
    self._sequence = None
    self._tools = None
    if parent is not None:
      self._add_to_parent(parent)
    else:
      self.parent = None
      if parser is None:
        # assume that this script is called from the JO
        self.parser = AthenaArgumentParser(stack_depth=stack_depth, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
      else:
        self.parser = parser
    group = self.parser.add_argument_group(title, description)
    self._output_streams = []
    self._declare_commandline_arguments(group)
    self._children = []


  def _add_to_parent(self, parent):
    """Add this parser as a child parser of parent"""
    parent._add_child(self)
    self.parser = parent.parser
    self.parent = parent

  def _add_child(self, child):
    self._children.append(child)

  def has_child(self, child_title):
    return any(child.title == child_title for child in self._children)

  def get_child(self, child_title):
    try:
      return next(child for child in self._children if child.title == child_title)
    except StopIteration:
      raise KeyError(child_title)

  def _declare_commandline_arguments(self, arg_group):
    """Declare the command line arguments. Should be implemented by derived classes"""
    pass

  def declare_stream(self, stream_var_name):
    self._output_streams.append(stream_var_name)

  def _autoconfigure(self):
    """Autoconfigure extra values based on input command line arguments and read metadata.
      Should be implemented by derivated classes
    """
    pass

  def parse_args(self, args = None):
    namespace = JobConfigurationValues()
    self._set_opts(self.parser.parse_args(args, namespace) )
    return self.opts

  def get_output_streams(self):
    # if multiple configs declare the same stream it's only added once. All the output files will then
    # be sent to the same stream. If running locally the output file will be named by the first config
    # to name the stream
    known_streams = set()
    outputs = []
    def read_streams_from(obj):
      for stream in obj._output_streams:
        stream_string = getattr(obj.opts, stream.replace('-', '_') )
        stream_name = stream_string.partition(':')[0]
        if stream_name in known_streams:
          continue
        else:
          known_streams.add(stream_name)
          outputs.append(stream_string)
    read_streams_from(self)
    for child in self._children:
      read_streams_from(child)
    return outputs


  def _set_opts(self, opts):
    self.opts = opts
    self._on_parse()
    for child in self._children:
      child._set_opts(opts)

  def _on_parse(self):
    """
      Function to be called after parsing. Resolve path names, check validity
      of parameters. Anything that can be done as soon as possible but without
      file metadata
    """
    pass


  def read_metadata(self, input_files = None, infos = None):
    """Read metadata from input files. Must be called after files have been loaded (i.e. after 
      calling 'import AthenaRootComps.ReadAthenaxAODHybrid' or similar line.
    """
    if infos is None:
      if input_files is None:
        # Get them from the svcMgr
        from __main__ import svcMgr
        input_files = svcMgr.EventSelector.InputCollections
      if len(input_files) == 0:
        raise IOError("No input files loaded!")
      self.athfile = None
      # Find the first file containing events
      for file_name in input_files:
        this_file = self._metadata_reader_class.from_fname(file_name)
        if this_file.nentries > 0:
          self.athfile = this_file
          break
      if self.athfile is None:
        logger.warning("All input files are empty. Will use metadata from the first but it might be faulty")
        self.athfile = self._metadata_reader_class.from_fname(input_files[0])
      infos = self.athfile.fileinfos
    else:
      self.athfile = self._metadata_reader_class.from_infos(infos)
    self._autoconfigure()
    for child in self._children:
      child.read_metadata(infos=infos)
