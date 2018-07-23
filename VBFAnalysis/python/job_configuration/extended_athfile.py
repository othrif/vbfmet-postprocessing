#from PyUtils.AthFile.module import AthFile
import PyUtils.AthFile
AthFile = PyUtils.AthFile.module.AthFile

class ExtendedAthFile(AthFile):
  """Extension to the base AthFile class to allow reading more sophisticated metadata"""

  __slots__ = ()

  @classmethod
  def from_infos(cls, infos):
    o = cls()
    o.fileinfos = PyUtils.AthFile.module.impl._create_file_infos()
    o.fileinfos.update(infos.copy() )
    return o

  @classmethod
  def from_fname(cls, fname):
    o = AthFile.from_fname(fname)
    return cls.from_infos(o.fileinfos)

  @classmethod
  def get_first_nonempty(cls, file_list):
    for file_name in file_list:
      fp = cls.from_fname(file_name)
      if fp.nentries > 0:
        return fp
    return None

  @property
  def project(self):
    return self.infos['tag_info']['project_name']

  @property
  def is_mc(self):
    return self.project == 'IS_SIMULATION'

  @property
  def is_atlfastII(self):
    if not self.is_mc:
      return False
    else:
      return "ATLFASTII" in self.infos['metadata']['/Simulation/Parameters']['SimulationFlavour']

  @property
  def year(self):
    if self.is_mc:
      return None
    else:
      return int(self.project[4:6])

  @property
  def file_type(self):
    data_items = self.infos['eventdata_items']
    try:
      data_header = next(i for i in reversed(data_items) if i[0] == "DataHeader")[1]
    except StopIteration:
      raise KeyError("Key DataHeader not present in 'eventdata_items'")
    if data_header.startswith("Stream"):
      data_header = data_header[6:]
    return data_header

  @property
  def stream_name(self):
    return self.infos['det_descr_tags']['triggerStreamOfFile']

  @property
  def ami_tags(self):
    return set(self.infos['tag_info']['AMITag'].split('_'))

  @property
  def mc_project(self):
    if not self.is_mc:
      return None
    tags = self.ami_tags
    # These tags are taken from the MC Production Group twiki pages
    if   'r9364'  in tags: return 'mc16a'
    elif 'r9297'  in tags: return 'mc16b'
    elif 'r9781'  in tags: return 'mc16c'
    elif 'r10210' in tags: return 'mc16d'
    else:
      raise ValueError("Unable to deduce MC campaign from AMI tags {0}".format(tags) )
