"""

This module configures input files

"""

import os
import re
import sys
import operator
import HInvPlot.Vars as get_vars
import HInvPlot.systematics as systematics

#import PyCintex,
import ROOT

import HInvPlot.JobOptions as config

log = config.getLog('Input.py')

#-------------------------------------------------------------------------
class ReadEvent:
    """ ReadEvent -  read events """

    def __init__(self, alg_name, options, my_files, my_runs_map, syst_name):

        self.name       = alg_name
        self.read_reg   = ROOT.Msl.Registry()
        self.read_alg   = ROOT.Msl.ReadEvent()
        self.algs       = []
        self.trees      = options.trees.split(',')
        self.files      = my_files

        self.read_reg.SetVal('ReadEvent::Name',          alg_name)
        self.read_reg.SetVal('ReadEvent::Print',         options.print_alg)
        self.read_reg.SetVal('ReadEvent::PrintEvent',    options.print_evt)
        self.read_reg.SetVal('ReadEvent::Debug',         options.debug_alg)
        self.read_reg.SetVal('ReadEvent::MaxNEvent',     options.nevent)
        self.read_reg.SetVal('ReadEvent::Year',          options.year)
        self.read_reg.SetVal('ReadEvent::LumiInt',       options.int_lumi)
        self.read_reg.SetVal('ReadEvent::MCEventCount',  options.mc_evt_count)
        self.read_reg.SetVal('ReadEvent::Skim',          options.skim)
        self.read_reg.SetVal('ReadEvent::Lumi',          options.int_lumi)
        self.read_reg.SetVal('ReadEvent::METChoice',     options.met_choice)
        self.read_reg.SetVal('ReadEvent::JetVetoPt',     options.jet_veto_pt)
        self.read_reg.SetVal('ReadEvent::LoadBaseLep',   options.LoadBaseLep)
        self.read_reg.SetVal('ReadEvent::OverlapPh',     options.OverlapPh)
        self.read_reg.SetVal('ReadEvent::BTagCut',       options.BTagCut)
        self.read_reg.SetVal('ReadEvent::TMVAWeightPath',options.mva_weights_path)
        self.read_reg.SetVal('ReadEvent::TrigString',    options.trig_name)  # specify a trigger from the command line
        self.read_reg.SetVal('ReadEvent::mergePTV',      options.mergePTV)
        self.read_reg.SetVal('ReadEvent::mergeExt',      options.mergeExt)
        self.read_reg.SetVal('ReadEvent::noVjWeight',      options.noVjWeight)
        self.read_reg.SetVal('ReadEvent::Year',          options.year)          

        self.read_reg.SetVal('ReadEvent::Print',      'yes')
        self.read_reg.SetVal('ReadEvent::Trees',      ' '.join(self.trees))
        self.read_reg.SetVal('ReadEvent::Files',      ' '.join(self.files))

        self.read_reg.SetVal('ReadEvent::MCIDs',      ' '.join(my_runs_map.keys()))
        self.read_reg.SetVal('ReadEvent::Samples',    ' '.join(my_runs_map.values()))
        self.read_reg.SetVal('ReadEvent::InputCount', -1.0) # 9983282

        self.read_reg.SetVal('ReadEvent::Sumw',options.sumw)
        self.read_reg.SetVal('ReadEvent::Nraw',options.nraw)

        # Load the systematics
        syst_class = systematics.systematics('All')
        #self.read_reg.SetVal('ReadEvent::SystList',','.join(syst_class.getsystematicsList()))

        if options.cfile != None:
            self.read_reg.SetVal('ReadEvent::CutFlowFile', options.cfile)

            rawfile = None
            if   options.cfile.count('txt'): rawfile = options.cfile.replace('txt', 'raw')
            elif options.cfile.count('cut'): rawfile = options.cfile.replace('cut', 'raw')

            if rawfile:
                self.read_reg.SetVal('ReadEvent::RawFlowFile', rawfile)

        all_runs = []

        self.read_reg.SetVal('ReadEvent::AllRuns',    ','.join(sorted(all_runs)))

        #
        # Additional input variables
        #    - read branches from tree and add to Event::VarHolder as enums
        #
        inp_vars = get_vars.GetVarStr(0, syst_name)
        mev_vars = get_vars.mev_vars
        self.read_reg.SetVal('ReadEvent::InputVars', ','.join(sorted(inp_vars)))
        self.read_reg.SetVal('ReadEvent::VarMeV',    ','.join(sorted(mev_vars)))

        #
        # Configure self
        #
        self.read_alg.Conf(self.read_reg)

    def SetTrees(self,trees):
        self.trees = trees

    def ClearAlgs(self):
        self.algs=[]
        self.read_alg.ClearAlgs()

    def SetSystName(self,systName):
        self.read_alg.SetSystName(systName)
    def SetWeightSystName(self,systName):
        self.read_alg.SetWeightSystName(systName)

    def ReadFile(self, path):

        if not os.path.exists(path):
            log.warning('ReadFile - could not find file: %s' %path)
            return None

        self.read_alg.Read(path)

    def ReadAllFiles(self):
        # Files are passed in the config
        for path in self.files:
            if not os.path.exists(path):
                log.warning('ReadFile - could not find file: %s' %path)
                return None

        self.read_alg.ReadAllFile()

    def Save(self, rfile, dirname = None, writeStyle='RECREATE'):
        if type(rfile) != type(''):
            self.read_alg.Save(0)
            return

        rfile = ROOT.TFile(rfile, writeStyle)

        log.info('ReadEvent - save algorithms...')

        if type(dirname) == type(''):
            self.read_alg.Save(rfile.mkdir('%s' %(dirname)))
        else:
            self.read_alg.Save(rfile)

        log.info('ReadEvent - write file...')

        rfile.Write()
        rfile.Close()
        del rfile

    def ConvertAlgToList(self, par):
        if type(par) == type([]):
            return par
        if par != None and hasattr(par, 'GetCppExecAlg'):
            return [par]
        return []

    def AddCommonAlg(self, alg):
        for a in self.ConvertAlgToList(alg):
            self.read_alg.AddCommonAlg(a.GetCppExecAlg())
            self.algs += [a]

    def AddNormalAlg(self, key, alg):
        for a in self.ConvertAlgToList(alg):

            if hasattr(a, 'GetCppExecAlg'):
                self.read_alg.AddNormalAlg(key, a.GetCppExecAlg())
                self.algs += [a]
            else:
                raise TypeError('AddNormalAlg - unknown type: %s' %a)

    def AddPreSelAlg(self, key, alg):
        for a in self.ConvertAlgToList(alg):
            self.read_alg.AddPreSelAlg(key, a.GetCppExecAlg())
            self.algs += [a]

    def GetName(self):
        return self.name

    def PrintAlgs(self):
        return self.read_alg.PrintAlgs()

    def RunConfForAlgs(self):
        return self.read_alg.RunConfForAlgs()

#-------------------------------------------------------------------------
def _processSimlNtupleDir(path, syst, runs):
    """
    Recursive function - collect all files that match run numbers and systematics
    """

    files = {}

    if not os.path.isdir(path):
        return files

    for file in os.listdir(path):
        fpath = path.rstrip('/')+'/'+file

        if os.path.isdir(fpath) and len(file) > 2:
            results = _processSimlNtupleDir(fpath, syst, runs)

            for run, val in results.iteritems():
                if run in files:
                    log.warning('processSimlNtupleDir - 0: skip duplicate run %s: %s' %(run, fpath))
                else:
                    files[run] = val
            continue

        if not os.path.isfile(fpath):
            continue

        if file.count('root') == 0:
            continue

        if syst != None:
            parts = fpath.split('/')

            #
            # Always require correct systematics key for MC
            #
            if syst not in parts and ('%s_MVA' %syst) not in parts:
                continue

        for run in runs:
            if file.count(run):
                if run in files.iteritems():
                    log.warning('processSimlNtupleDir - 1: skip duplicate run %s: %s' %(run, fpath))
                else:
                    files[run] = fpath

    return files

#-------------------------------------------------------------------------
def getInputSimlFiles(input_file,file_list, printFiles=False):
    """
    Collect input MC files:
      - match run numbers and systematic name
      - check for missing run numbers
    """

    files = []
    if input_file :
        try:
            f=open(input_file)
        except IOError:
            log.error('Failed to open the file with the list of input files: %s' %input_file)
            raise NameError('Could not find file. Check input!')

        for i in f:
            if i.count('#'):
                print 'skipping because of comment #: ',i
                continue
            if i not in files and len(i.strip())>0:
                files.append(i.strip())
                if printFiles:
                    log.info('Input File: %s' %i)
        f.close()

    elif file_list :
        files = file_list.split(',')

    return files

#-------------------------------------------------------------------------
def _processDataNtupleDir(path):
    """
    Recursive function - collect all data files
    """

    files = []

    if not os.path.isdir(path):
        return files

    for file in os.listdir(path):
        fpath = path.rstrip('/')+'/'+file
        print 'file: ',file
        if fpath.lower().count('data') == 0:
            continue

        if os.path.isdir(fpath) and len(file) > 2:
            files += _processDataNtupleDir(fpath)
            continue

        if os.path.isfile(fpath) and file.count('root'):
            files += [fpath]

    return files

#-------------------------------------------------------------------------
def getInputDataFiles(paths):
    """
    Collect input data files:
      - match period
    """

    results = []
    inputs  = []

    if type(paths) == type(''):
        paths = [paths]

    for path in paths:
        if os.path.isdir(path):
            if path.count('ntupleOutput'):
                inputs += [path]
            else:
                for input in os.listdir(path):
                    inputs += ['%s/%s' %(path.rstrip('/'), input)]

    for path in inputs:

        if not os.path.isdir(path):
            log.debug('getInputDataFiles - path is not directory: %s' %path)
            continue

        if path.count('ntupleOutput') == 0:
            continue

        files = []

        for file in os.listdir(path):
            fpath = path.rstrip('/')+'/'+file

            if os.path.isdir(fpath):

                #if fpath.count('data_all'):
                if fpath.count('/data') or fpath.count('/allData'):
                    files += _processDataNtupleDir(fpath)

        results += files

        log.info('getInputDataFiles - processed input directory:')
        log.info('                    path: %s'         %path)
        log.info('                    added %d file(s)' %len(files))

        log.info('getInputDataFiles - added %d file(s):'  %len(files))
        for file in files:
            log.info('                    %s' %file)

    return results

#-------------------------------------------------------------------------
# Create map from sample keys to run numbers
#
def prepareBkgRuns(keys,options=None):

        #
        #
        #
    sig_tth125    = {'346632':'1l',
                     '346633':'0l',
                     '346634':'2l',}
    sig_VH125     = {'308072':'ZH125',
                     '308071':'WpH125',
                     '308070':'WmH125',
                     '345038':'ZH125 - new incl',
                     '345039':'WpH125 - new incl',
                     '345040':'WmH125 - new incl',
                     '346605':'WpinclHinv_MET75',
                     '346606':'WminclHinv_MET75',
                     '346607':'ZinclHinv_MET75',
                     '345596':'ggZinclHinv_MET75',
    }

    sig_ggF125 = {'308284':'ggF125',
                  '346588':'ggF125 reshower',}
    #sig_ggF125 = {'364162':'Wmunu_MAXHTPTV140_280_CVetoBVeto',}
    #sig_VH125     = {'364106':'TBD',}
    #sig_VH125v2     = {'364148':'TBD',}
    sig_VBF125     = {'308276':'VBF125 - met',
                      '308567':'VBF125 - all',
                      '346600':'VBF125 - met>75',
                          }
    sig_vbfgam = {'312243':'vbf gamma', }
    alt_VBF = {'308275':'VBF125 - H75',
               '308277':'VBF125 - H200',
               '308278':'VBF125 - H300',
               #'308279':'VBF125 - H500', 
               '308280':'VBF125 - H750', 
               #'308281':'VBF125 - H1000',
               '308282':'VBF125 - H2000',
               #'308283':'VBF125 - H3000',
                   }

    bkg_wewk =     {'308096':'WenuEWK',
                    '308097':'WmunuEWK',
                    '308098':'WtaunuEWK',
                        }
    bkg_wewkpow =     {'363237':'WenuEWK',
                       '363238':'WmunuEWK',
                       '363239':'WtaunuEWK',
                        }

    bkg_zgewk =     {'363266':'ZnnEWK',
                    '363267':'ZeeEWK',
                    '363268':'ZmmEWK',
                    '363269':'ZttEWK',
                        }

    bkg_wgewk =     {'363270':'WenEWK',
                     '363271':'WmnEWK',
                     '363272':'WtnEWK',  }

    bkg_new = {#'312243':'',
                   '343982':'',
                   '343983':'',
                   '343984':'',
                   '343985':'',
                   '343986':'',
                   }
    bkg_zee_228 = {'421301':'zee_ptvEnh'}
    bkg_zqcd_LO_Filt = {    '311429':'Znunu_TightVBF_Np01',
                            '311430':'Znunu_TightVBF_Np2',
                            '311431':'Znunu_TightVBF_Np3',
                            '311432':'Znunu_TightVBF_Np4',
                            '311433':'Zee_TightVBF_Np01',
                            '311434':'Zee_TightVBF_Np2',
                            '311435':'Zee_TightVBF_Np3',
                            '311436':'Zee_TightVBF_Np4',
                            '311437':'Zmumu_TightVBF_Np01',
                            '311438':'Zmumu_TightVBF_Np2',
                            '311439':'Zmumu_TightVBF_Np3',
                            '311440':'Zmumu_TightVBF_Np4',
                            '311441':'Ztautau_TightVBF_Np01',
                            '311442':'Ztautau_TightVBF_Np2',
                            '311443':'Ztautau_TightVBF_Np3',
                            '311444':'Ztautau_TightVBF_Np4',
                            }

    bkg_wqcd_LO_Filt = {'311445':'Wenu_Ht140_280_13TeV_BVCVVBF',
                       '311446':'Wmunu_Ht140_280_13TeV_BVCVVBF',
                       '311447':'Wenu_Ht280_500_13TeV_BVCVVBF',
                       '311448':'Wmunu_Ht280_500_13TeV_BVCVVBF',
                       '311449':'Wtaunu_Ht140_280_13TeV_BVCVVBF',
                       '311450':'Wtaunu_Ht280_500_13TeV_BVCVVB',
                       '311451':'Wenu_Ht700_13TeV_VBF',
                       '311452':'Wmunu_Ht700_13TeV_VBF',
                       '311453':'Wtaunu_Ht500_13TeV_VBF',
                           }

    bkg_wqcd_mnu =     {'364156':'Wmunu_MAXHTPTV0_70_CVetoBVeto',
                    '364157':'Wmunu_MAXHTPTV0_70_CFilterBVeto',
                    '364158':'Wmunu_MAXHTPTV0_70_BFilter',
                    '364159':'Wmunu_MAXHTPTV70_140_CVetoBVeto',
                    '364160':'Wmunu_MAXHTPTV70_140_CFilterBVeto',
                    '364161':'Wmunu_MAXHTPTV70_140_BFilter',
                    '364162':'Wmunu_MAXHTPTV140_280_CVetoBVeto',
                    '364163':'Wmunu_MAXHTPTV140_280_CFilterBVeto',
                    '364164':'Wmunu_MAXHTPTV140_280_BFilter',
                    '364165':'Wmunu_MAXHTPTV280_500_CVetoBVeto',
                    '364166':'Wmunu_MAXHTPTV280_500_CFilterBVeto',
                    '364167':'Wmunu_MAXHTPTV280_500_BFilter',
                    '364168':'Wmunu_MAXHTPTV500_1000',
                    '364169':'Wmunu_MAXHTPTV1000_E_CMS',  }
    bkg_wqcd_enu={'364170':'Wenu_MAXHTPTV0_70_CVetoBVeto',
                    '364171':'Wenu_MAXHTPTV0_70_CFilterBVeto',
                    '364172':'Wenu_MAXHTPTV0_70_BFilter',
                    '364173':'Wenu_MAXHTPTV70_140_CVetoBVeto',
                    '364174':'Wenu_MAXHTPTV70_140_CFilterBVeto',
                    '364175':'Wenu_MAXHTPTV70_140_BFilter',
                    '364176':'Wenu_MAXHTPTV140_280_CVetoBVeto',
                    '364177':'Wenu_MAXHTPTV140_280_CFilterBVeto',
                    '364178':'Wenu_MAXHTPTV140_280_BFilter',
                    '364179':'Wenu_MAXHTPTV280_500_CVetoBVeto',
                    '364180':'Wenu_MAXHTPTV280_500_CFilterBVeto',
                    '364181':'Wenu_MAXHTPTV280_500_BFilter',
                    '364182':'Wenu_MAXHTPTV500_1000',
                    '364183':'Wenu_MAXHTPTV1000_E_CMS',   }
    bkg_wqcd_tnu={'364184':'Wtaunu_MAXHTPTV0_70_CVetoBVeto',
                    '364185':'Wtaunu_MAXHTPTV0_70_CFilterBVeto',
                    '364186':'Wtaunu_MAXHTPTV0_70_BFilter',
                    '364187':'Wtaunu_MAXHTPTV70_140_CVetoBVeto',
                    '364188':'Wtaunu_MAXHTPTV70_140_CFilterBVeto',
                    '364189':'Wtaunu_MAXHTPTV70_140_BFilter',
                    '364190':'Wtaunu_MAXHTPTV140_280_CVetoBVeto',
                    '364191':'Wtaunu_MAXHTPTV140_280_CFilterBVeto',
                    '364192':'Wtaunu_MAXHTPTV140_280_BFilter',
                    '364193':'Wtaunu_MAXHTPTV280_500_CVetoBVeto',
                    '364194':'Wtaunu_MAXHTPTV280_500_CFilterBVeto',
                    '364195':'Wtaunu_MAXHTPTV280_500_BFilter',
                    '364196':'Wtaunu_MAXHTPTV500_1000',
                    '364197':'Wtaunu_MAXHTPTV1000_E_CMS',
                        }
    bkg_wqcd={}
    bkg_wqcd.update(bkg_wqcd_enu)
    bkg_wqcd.update(bkg_wqcd_mnu)
    bkg_wqcd.update(bkg_wqcd_tnu)
    bkg_zewk =     {'308092':'ZeeEWK',
                    '308093':'ZmmEWK',
                    '308094':'ZttEWK',
                    '308095':'ZnnEWK',
                        }

    bkg_zewkpow =     {'363234':'ZeeEWK',
                       '363235':'ZmmEWK',
                       '363236':'ZttEWK',
                       '363233':'ZnnEWK',
                   }

    bkg_zqcd_zmm = {'364100':'Zmumu_MAXHTPTV0_70_CVetoBVeto',
                    '364101':'TBD',
                    '364102':'TBD',
                    '364103':'TBD',#70 _CVetoBVeto
                    '364104':'TBD',
                    '364105':'TBD',
                    '364106':'TBD',#140
                    '364107':'TBD',
                    '364108':'TBD',
                    '364109':'TBD',
                    '364110':'TBD',
                    '364111':'TBD',
                    '364112':'TBD',
                    '364113':'TBD',}
    bkg_zqcd_zee = {'364114':'Zee_MAXHTPTV0_70_CVetoBVeto',
                    '364115':'TBD',
                    '364116':'TBD',
                    '364117':'TBD',#70
                    '364118':'TBD',
                    '364119':'TBD',
                    '364120':'TBD',#140
                    '364121':'Zee_MAXHTPTV140_280_CFilterBVeto',
                    '364122':'TBD',
                    '364123':'TBD',
                    '364124':'TBD',
                    '364125':'TBD',
                    '364126':'TBD',
                    '364127':'TBD',}
    bkg_zqcd_ztt = {'364128':'Ztautau_MAXHTPTV0_70_CVetoBVeto',
                    '364129':'TBD',
                    '364130':'TBD',
                    '364131':'TBD',#70
                    '364132':'TBD',
                    '364133':'TBD',
                    '364134':'TBD',#140
                    '364135':'TBD',
                    '364136':'TBD',
                    '364137':'TBD',#280
                    '364138':'TBD',
                    '364139':'TBD',
                    '364140':'TBD',
                    '364141':'TBD',}
    bkg_zqcd_znn = {'364142':'Znunu_MAXHTPTV0_70_CVetoBVeto',
                    '364143':'TBD',
                    '364144':'TBD',
                    '364145':'TBD',#70 CVBV
                    '364146':'TBD',
                    '364147':'TBD',
                    '364148':'TBD',#140
                    '364149':'TBD',
                    '364150':'TBD',
                    '364151':'TBD',#280
                    '364152':'TBD',
                    '364153':'TBD',
                    '364154':'TBD',
                    '364155':'Znunu_MAXHTPTV1000',
                    }
    bkg_zqcd_znn_mc16e = {                # mc16e samples
                    '366010':'pt70bfilter',
                    '366011':'pt100',
                    '366012':'pt100',
                    '366013':'pt100',
                    '366014':'pt140',
                    '366015':'pt140',
                    '366016':'pt140',
                    '366017':'pt280',
                    '366018':'pt280',
                    '366019':'pt70cfilterVBV',
                    '366020':'pt100',
                    '366021':'pt100',
                    '366022':'pt100',
                    '366023':'pt140',
                    '366024':'pt140',
                    '366025':'pt140',
                    '366026':'pt280',
                    #'366027':'pt280', # does not exist
                    '366028':'pt70CVBV',
                    '366029':'pt100',
                    '366030':'pt100',
                    '366031':'pt100',
                    '366032':'pt140',
                    '366033':'pt140',
                    '366034':'pt140',
                    '366035':'pt280',
                    }

    bkg_zqcd_sh_ktExtalt = {'312448':'Zee_PTV100_140_MJJ0_500_KtMerging',
                         '312449':'Zee_PTV100_140_MJJ500_1000_KtMerging',
                         '312451':'Zee_PTV140_220_MJJ0_500_KtMerging',
                         '312452':'Zee_PTV140_220_MJJ500_1000_KtMerging',
                         '312460':'Zmm_PTV100_140_MJJ0_500_KtMerging',
                         '312461':'Zmm_PTV100_140_MJJ500_1000_KtMerging',
                         '312463':'Zmm_PTV140_220_MJJ0_500_KtMerging',
                         '312464':'Zmm_PTV140_220_MJJ500_1000_KtMerging',
                         '312472':'Ztt_PTV100_140_MJJ0_500_KtMerging',
                         '312473':'Ztt_PTV100_140_MJJ500_1000_KtMerging',
                         '312475':'Ztt_PTV140_220_MJJ0_500_KtMerging',
                         '312476':'Ztt_PTV140_220_MJJ500_1000_KtMerging',
                         '312484':'Znunu_PTV100_140_MJJ0_500_KtMerging',
                         '312485':'Znunu_PTV100_140_MJJ500_1000_KtMerging',
                         '312487':'Znunu_PTV140_220_MJJ0_500_KtMerging',
                         '312488':'Znunu_PTV140_220_MJJ500_1000_KtMerging',                         
                                }
    bkg_zqcd_sh_ktExt = {#'312448':'Zee_PTV100_140_MJJ0_500_KtMerging',
                         #'312449':'Zee_PTV100_140_MJJ500_1000_KtMerging',
                         '312450':'Zee_PTV100_140_MJJ1000__E_CMS_KtMerging',
                         #'312451':'Zee_PTV140_220_MJJ0_500_KtMerging',
                         #'312452':'Zee_PTV140_220_MJJ500_1000_KtMerging',
                         '312453':'Zee_PTV140_220_MJJ1000__E_CMS_KtMerging',
                         '312454':'Zee_PTV220_280_MJJ0_500_KtMerging',
                         '312455':'Zee_PTV220_280_MJJ500_1000_KtMerging',
                         '312456':'Zee_PTV220_280_MJJ1000__E_CMS_KtMerging',
                         '312457':'Zee_PTV280_500_MJJ0_500_KtMerging',
                         '312458':'Zee_PTV280_500_MJJ500_1000_KtMerging',
                         '312459':'Zee_PTV280_500_MJJ1000__E_CMS_KtMerging',
                         #'312460':'Zmm_PTV100_140_MJJ0_500_KtMerging',
                         #'312461':'Zmm_PTV100_140_MJJ500_1000_KtMerging',
                         '312462':'Zmm_PTV100_140_MJJ1000__E_CMS_KtMerging',
                         #'312463':'Zmm_PTV140_220_MJJ0_500_KtMerging',
                         #'312464':'Zmm_PTV140_220_MJJ500_1000_KtMerging',
                         '312465':'Zmm_PTV140_220_MJJ1000__E_CMS_KtMerging',
                         '312466':'Zmm_PTV220_280_MJJ0_500_KtMerging',
                         '312467':'Zmm_PTV220_280_MJJ500_1000_KtMerging',
                         '312468':'Zmm_PTV220_280_MJJ1000__E_CMS_KtMerging',
                         '312469':'Zmm_PTV280_500_MJJ0_500_KtMerging',
                         '312470':'Zmm_PTV280_500_MJJ500_1000_KtMerging',
                         '312471':'Zmm_PTV280_500_MJJ1000__E_CMS_KtMerging',
                         #'312472':'Ztt_PTV100_140_MJJ0_500_KtMerging',
                         #'312473':'Ztt_PTV100_140_MJJ500_1000_KtMerging',
                         '312474':'Ztt_PTV100_140_MJJ1000__E_CMS_KtMerging',
                         #'312475':'Ztt_PTV140_220_MJJ0_500_KtMerging',
                         #'312476':'Ztt_PTV140_220_MJJ500_1000_KtMerging',
                         '312477':'Ztt_PTV140_220_MJJ1000__E_CMS_KtMerging',
                         '312478':'Ztt_PTV220_280_MJJ0_500_KtMerging',
                         '312479':'Ztt_PTV220_280_MJJ500_1000_KtMerging',
                         '312480':'Ztt_PTV220_280_MJJ1000__E_CMS_KtMerging',
                         '312481':'Ztt_PTV280_500_MJJ0_500_KtMerging',
                         '312482':'Ztt_PTV280_500_MJJ500_1000_KtMerging',
                         '312483':'Ztt_PTV280_500_MJJ1000__E_CMS_KtMerging',
                         #'312484':'Znunu_PTV100_140_MJJ0_500_KtMerging',
                         #'312485':'Znunu_PTV100_140_MJJ500_1000_KtMerging',
                         '312486':'Znunu_PTV100_140_MJJ1000__E_CMS_KtMerging',
                         #'312487':'Znunu_PTV140_220_MJJ0_500_KtMerging',
                         #'312488':'Znunu_PTV140_220_MJJ500_1000_KtMerging',
                         '312489':'Znunu_PTV140_220_MJJ1000__E_CMS_KtMerging',
                         '312490':'Znunu_PTV220_280_MJJ0_500_KtMerging',
                         '312491':'Znunu_PTV220_280_MJJ500_1000_KtMerging',
                         '312492':'Znunu_PTV220_280_MJJ1000__E_CMS_KtMerging',
                         '312493':'Znunu_PTV280_500_MJJ0_500_KtMerging',
                         '312494':'Znunu_PTV280_500_MJJ500_1000_KtMerging',
                         '312495':'Znunu_PTV280_500_MJJ1000__E_CMS_KtMerging',
                     }
    bkg_zqcd_sh_ktExt.update(bkg_zqcd_sh_ktExtalt)
    bkg_wqcd_sh_ktExt = {
                         '312496':'Wenu_PTV100_140_MJJ0_500_KtMerging',
                         '312497':'Wenu_PTV100_140_MJJ500_1000_KtMerging',
                         '312498':'Wenu_PTV100_140_MJJ1000__E_CMS_KtMerging',
                         '312499':'Wenu_PTV140_220_MJJ0_500_KtMerging',
                         '312500':'Wenu_PTV140_220_MJJ500_1000_KtMerging',
                         '312501':'Wenu_PTV140_220_MJJ1000__E_CMS_KtMerging',
                         '312502':'Wenu_PTV220_280_MJJ0_500_KtMerging',
                         '312503':'Wenu_PTV220_280_MJJ500_1000_KtMerging',
                         '312504':'Wenu_PTV220_280_MJJ1000__E_CMS_KtMerging',
                         '312505':'Wenu_PTV280_500_MJJ0_500_KtMerging',
                         '312506':'Wenu_PTV280_500_MJJ500_1000_KtMerging',
                         '312507':'Wenu_PTV280_500_MJJ1000__E_CMS_KtMerging',
                         '312508':'Wmunu_PTV100_140_MJJ0_500_KtMerging',
                         '312509':'Wmunu_PTV100_140_MJJ500_1000_KtMerging',
                         '312510':'Wmunu_PTV100_140_MJJ1000__E_CMS_KtMerging',
                         '312511':'Wmunu_PTV140_220_MJJ0_500_KtMerging',
                         '312512':'Wmunu_PTV140_220_MJJ500_1000_KtMerging',
                         '312513':'Wmunu_PTV140_220_MJJ1000__E_CMS_KtMerging',
                         '312514':'Wmunu_PTV220_280_MJJ0_500_KtMerging',
                         '312515':'Wmunu_PTV220_280_MJJ500_1000_KtMerging',
                         '312516':'Wmunu_PTV220_280_MJJ1000__E_CMS_KtMerging',
                         '312517':'Wmunu_PTV280_500_MJJ0_500_KtMerging',
                         '312518':'Wmunu_PTV280_500_MJJ500_1000_KtMerging',
                         '312519':'Wmunu_PTV280_500_MJJ1000__E_CMS_KtMerging',
                         '312520':'Wtaunu_PTV100_140_MJJ0_500_KtMerging',
                         '312521':'Wtaunu_PTV100_140_MJJ500_1000_KtMerging',
                         '312522':'Wtaunu_PTV100_140_MJJ1000__E_CMS_KtMerging',
                         '312523':'Wtaunu_PTV140_220_MJJ0_500_KtMerging',
                         '312524':'Wtaunu_PTV140_220_MJJ500_1000_KtMerging',
                         '312525':'Wtaunu_PTV140_220_MJJ1000__E_CMS_KtMerging',
                         '312526':'Wtaunu_PTV220_280_MJJ0_500_KtMerging',
                         '312527':'Wtaunu_PTV220_280_MJJ500_1000_KtMerging',
                         '312528':'Wtaunu_PTV220_280_MJJ1000__E_CMS_KtMerging',
                         '312529':'Wtaunu_PTV280_500_MJJ0_500_KtMerging',
                         '312530':'Wtaunu_PTV280_500_MJJ500_1000_KtMerging',
                         '312531':'Wtaunu_PTV280_500_MJJ1000__E_CMS_KtMerging',
    }

    bkg_zqcd={}
    bkg_zqcd.update(bkg_zqcd_zmm)
    bkg_zqcd.update(bkg_zqcd_zee)
    bkg_zqcd.update(bkg_zqcd_ztt)
    if options.year==2018 or options.mergePTV:
        bkg_zqcd.update(bkg_zqcd_znn_mc16e)
    else:
        bkg_zqcd.update(bkg_zqcd_znn)

    bkg_top1 = {
        '117360':'tchan->e',
        '117361':'tchan->mu',
        '117362':'tchan->tau',
        '108343':'schan->e',
        '108344':'schan->mu',
        '108345':'schan->tau',
        '108346':'Wt',
        }
    bkg_top2 = {
        '410470':'ttbar(w/oFullHad)',
        '410471':'ttbar(w/FullHad)',
        #'410472':'ttbar(w/dil)',                remove dilepton
        }
    bkg_top1 = {
        '410011':'tchan_top',
        '410012':'tchan_antitop',
        '410013':'Wt_top',
        '410014':'Wt_top',
        '410025':'schan_top',
        '410026':'schan_antitop',
        }
    bkg_top1 = {
        '410642':'tchan_lept_top',
        '410643':'tchan_lept_antitop',
        '410644':'schan_top_lept',
        '410645':'schan_antitop_lept',
        '410646':'Wt_top_incl',
        '410647':'Wt_antitop_incl',
        #'410648':'Wt_DR_dilepton_top',
        #'410649':'Wt_DR_dilepton_antitop',
        }

    # default!!! Powheg+Pythia 8
    bkg_top1 = {
        '410658':'tchan_top', #lepton filtered
        '410659':'tchan_antitop',
        '410644':'schan_top',
        '410645':'schan_antitop',
        '410646':'Wt_top',
        '410647':'Wt_top',
        } #410643,410642,410648,410649

    bkg_top2.update(bkg_top1)
    bkg_top_other = {'410472':'ttbar(w/dil)',#                remove dilepton
                     '410648':'Wt_DR_dilepton_top',
                     '410649':'Wt_DR_dilepton_antitop',
                     '410642':'tchan_lept_top',
                     '410643':'tchan_lept_antitop',
                     #'410644':'schan_top_lept',
                     #'410645':'schan_antitop_lept',
                     #'410646':'Wt_top_incl',
                     #'410647':'Wt_antitop_incl',
        }
    bkg_z_strong_madgraph_znn = {'361515':'Znn_Np0',
                      '361516':'Znn_Np1',
                      '361517':'Znn_Np2',
                      '361518':'Znn_Np3',
                      '361519':'Znn_Np4',}
    bkg_z_strong_madgraph_ztt = {'361510':'Ztautau_Np0',
                      '361511':'Ztautau_Np1',
                      '361512':'Ztautau_Np2',
                      '361513':'Ztautau_Np3',
                      '361514':'Ztautau_Np4',
                      }
    bkg_z_strong_madgraph_zmm = {'363123':'Zmumu_Ht0_70_CVetoBVeto',
                      '363124':'BTD',
                      '363125':'BTD',
                      '363126':'BTD',
                      '363127':'BTD',
                      '363128':'BTD',
                      '363129':'BTD',
                      '363130':'BTD',
                      '363131':'BTD',
                      '363132':'BTD',
                      '363133':'BTD',
                      '363134':'BTD',
                      '363135':'BTD',
                      '363136':'BTD',
                      '363137':'BTD',
                      '363138':'BTD',
                      '363139':'BTD',
                      '363140':'BTD',
                      '363141':'BTD',
                      '363142':'BTD',
                      '363143':'BTD',
                      '363144':'BTD',
                      '363145':'BTD',
                      '363146':'BTD',}
    bkg_z_strong_madgraph_zee = {'363147':'Zee_Ht0_70_CVetoBVeto',
                      '363148':'BTD',
                      '363149':'BTD',
                      '363150':'BTD',
                      '363151':'BTD',
                      '363152':'BTD',
                      '363153':'BTD',
                      '363154':'BTD',
                      '363155':'BTD',
                      '363156':'BTD',
                      '363157':'BTD',
                      '363158':'BTD',
                      '363159':'BTD',
                      '363160':'BTD',
                      '363161':'BTD',
                      '363162':'BTD',
                      '363163':'BTD',
                      '363164':'BTD',
                      '363165':'BTD',
                      '363166':'BTD',
                      '363167':'BTD',
                      '363168':'BTD',
                      '363169':'BTD',
                      '363170':'BTD',
                      }
    bkg_z_strong_madgraph={}
    bkg_z_strong_madgraph.update(bkg_z_strong_madgraph_znn)
    bkg_z_strong_madgraph.update(bkg_z_strong_madgraph_zmm)
    bkg_z_strong_madgraph.update(bkg_z_strong_madgraph_ztt)
    bkg_z_strong_madgraph.update(bkg_z_strong_madgraph_zee)
    bkg_w_strong_madgraph_wmnu = {'363624':'Wmunu_Ht0_70_CVetoBVeto',
                      '363625':'BTD',
                      '363626':'BTD',
                      '363627':'BTD',
                      '363628':'BTD',
                      '363629':'BTD',
                      '363630':'BTD',
                      '363631':'BTD',
                      '363632':'BTD',
                      '363633':'BTD',
                      '363634':'BTD',
                      '363635':'BTD',
                      '363636':'BTD',
                      '363637':'BTD',
                      '363638':'BTD',
                      '363639':'BTD',
                      '363640':'BTD',
                      '363641':'BTD',
                      '363642':'BTD',
                      '363643':'BTD',
                      '363644':'BTD',
                      '363645':'BTD',
                      '363646':'BTD',
                      '363647':'BTD',}
    bkg_w_strong_madgraph_wenu={'363600':'Wenu_Ht0_70_CVetoBVeto',
                      '363601':'BTD',
                      '363602':'BTD',
                      '363603':'BTD',
                      '363604':'BTD',
                      '363605':'BTD',
                      '363606':'BTD',
                      '363607':'BTD',
                      '363608':'BTD',
                      '363609':'BTD',
                      '363610':'BTD',
                      '363611':'BTD',
                      '363612':'BTD',
                      '363613':'BTD',
                      '363614':'BTD',
                      '363615':'BTD',
                      '363616':'BTD',
                      '363617':'BTD',
                      '363618':'BTD',
                      '363619':'BTD',
                      '363620':'BTD',
                      '363621':'BTD',
                      '363622':'BTD',
                      '363623':'BTD',}
    bkg_w_strong_madgraph_wtnu={'363648':'Wtaunu_Ht0_70_CVetoBVeto',
                      '363649':'BTD',
                      '363650':'BTD',
                      '363651':'BTD',
                      '363652':'BTD',
                      '363653':'BTD',
                      '363654':'BTD',
                      '363655':'BTD',
                      '363656':'BTD',
                      '363657':'BTD',
                      '363658':'BTD',
                      '363659':'BTD',
                      '363660':'BTD',
                      '363661':'BTD',
                      '363662':'BTD',
                      '363663':'BTD',
                      '363664':'BTD',
                      '363665':'BTD',
                      '363666':'BTD',
                      '363667':'BTD',
                      '363668':'BTD',
                      '363669':'BTD',
                      '363670':'BTD',
                      '363671':'BTD',
                      }
    bkg_w_strong_madgraph={}
    bkg_w_strong_madgraph.update(bkg_w_strong_madgraph_wmnu)
    bkg_w_strong_madgraph.update(bkg_w_strong_madgraph_wenu)
    bkg_w_strong_madgraph.update(bkg_w_strong_madgraph_wtnu)
    bkg_z_strong_powheg = {'301020':'PowhegPythia8EvtGen_AZNLOCTEQ6L1_DYmumu_120M180',
                      '301021':'BTD',
                      '301022':'BTD',
                      '301023':'BTD',
                      '301024':'BTD',
                      '301025':'BTD',
                      '301026':'BTD',
                      '301027':'BTD',
                      '301028':'BTD',
                      '301029':'BTD',
                      '301030':'BTD',
                      '301031':'BTD',
                      '301032':'BTD',
                      '301033':'BTD',
                      '301034':'BTD',
                      '301035':'BTD',
                      '301036':'BTD',
                      '301037':'BTD',
                      '301038':'BTD',
                          }

    bkg_qcdunw = {'426001':'JZ1',
                    '426002':'JZ2',
                    '426003':'JZ3',
                    '426004':'JZ4',
                    '426005':'JZ5',
                    '426006':'JZ6',
                    '426007':'JZ7',
                    '426008':'JZ8',
                    '426009':'JZ9',
                    }
    bkg_datadriveqcd = {'-123':'Loose',}
    bkg_qcdw = {
                   '310502':'powerlaw',
                   '304784':'powerlaw',
                   '361020':'JZ0W',
                   '361021':'JZ1W',
                   '361022':'JZ2W',
                   '361023':'JZ3W',
                   '361024':'JZ4W',
                   '361025':'JZ5W',
                   '361026':'JZ6W',
                   '361027':'JZ7W',
                   '361028':'JZ8W',
                   '361029':'JZ9W',
                   '361030':'JZ10W',
                   '361031':'JZ11W',
                   '361032':'JZ12W',
                   }
    bkg_vv = {'364242':'3l3v_EWK6',
                  '364243':'4l2v_EWK6',
                  '364244':'WWZ_2l4v_EW6',
                  '364245':'WZZ_5l1v_EW6',
                  '364246':'WZZ_3l3v_EW6',
                  '364247':'ZZZ_6l0v_EW6',
                  '364248':'ZZZ_4l2v_EW6',
                  '364249':'ZZZ_2l4v_EW6',
                  # VV
                  '364253':'lllv',
                  '363494':'vvvv',
                  '364250':'llll',
                  '364254':'llvv',
                  '364255':'lvvv',
                  # possible samples to correlate with W/Z EWK?
                  '363359':'W+W-->qqln',
                  '363360':'W+W-->lnqq',
                  '363489':'WZ->lnqq',
                  '363355':'ZZ->qqnn',
                  '363356':'ZZ->qqll',
                  '363357':'WZ->qqnn',
                  '363358':'WZ->qqll',
                  # adding the VBFHWW tautau samples
                  '345948':'VBFHWW',
                  '346190':'VBFHtautaull',
                  '346191':'VBFHtautaulph',
                  '346192':'VBFHtautaulmh',
                  '346193':'VBFHtautauhh',
                  }

    bkg_vbfExt = {'309662':'Wenu_MAXHTPTV70_140',
                  '309663':'Wmunu_MAXHTPTV70_140',
                  '309664':'Wtaunu_MAXHTPTV70_140',
                  '309665':'Zmumu_MAXHTPTV70_140_CVBV',
                  '309666':'Ztautau_MAXHTPTV70_140_CFBV',
                  '309667':'Znunu_MAXHTPTV70_140_CVBV',
                  '309668':'Znunu_MAXHTPTV70_140_CFBV',
                  '309669':'Zmumu_MAXHTPTV140_280_CVBV',
                  '309670':'Zmumu_MAXHTPTV140_280_CFBV',
                  '309671':'Zee_MAXHTPTV140_280_CVBV',
                  '309672':'Ztautau_MAXHTPTV140_280_CVBV',
                  '309673':'Znunu_MAXHTPTV140_280_CVBV',
                  '309674':'Wmunu_MAXHTPTV140_280_CVBV',
                  '309675':'Wmunu_MAXHTPTV140_280_CFBV',
                  '309676':'Wenu_MAXHTPTV140_280_CVBV',
                  '309677':'Wenu_MAXHTPTV140_280_CFBV',
                  '309678':'Wtaunu_MAXHTPTV140_280_CVBV',
                  '309679':'Wtaunu_MAXHTPTV140_280_CFBV',
                      }

    bkg_vbfPTVExt = {'364216':'Zmumu_PTV500_1000',
                     '364217':'Zmumu_PTV1000_E_CMS',
                     '364218':'Zee_PTV500_1000',
                     '364219':'Zee_PTV1000_E_CMS',
                     '364220':'Ztautau_PTV500_1000',
                     '364221':'Ztautau_PTV1000_E_CMS',
                     '364222':'Znunu_PTV500_1000',
                     '364223':'Znunu_PTV1000_E_CMS',
                     '364224':'Wmunu_PTV500_1000',
                     '364225':'Wmunu_PTV1000_E_CMS',
                     '364226':'Wenu_PTV500_1000',
                     '364227':'Wenu_PTV1000_E_CMS',
                     '364228':'Wtaunu_PTV500_1000',
                     '364229':'Wtaunu_PTV1000_E_CMS',
                      }

    bkg_vbfFiltZ = {'345099':'TBD',
                    '345100':'TBD',
                    '345101':'TBD',
                    '345102':'TBD',}
    bkg_lowMassZ = {'364198':'TBD',
                        '364199':'TBD',
                        '364200':'TBD',
                        '364201':'TBD',
                        '364202':'TBD',
                        '364203':'TBD',
                        '364204':'TBD',
                        '364205':'TBD',
                        '364206':'TBD',
                        '364207':'TBD',
                        '364208':'TBD',
                        '364209':'TBD',
                        '364210':'TBD',
                        '364211':'TBD',
                        '364212':'TBD',
                        '364213':'TBD',
                        '364214':'TBD',
                        '364215':'TBD',
                        }
    bkg_sherpa_zg = {'364500':'eegamma_pty_7_15',
                     '364501':'eegamma_pty_15_35',
                     '364502':'eegamma_pty_35_70',
                     '364503':'eegamma_pty_70_140',
                     '364504':'eegamma_pty_140_E',
                     '364505':'mmgamma_pty_7_15',
                     '364506':'mmgamma_pty_15_35',
                     '364507':'mmgamma_pty_35_70',
                     '364508':'mmgamma_pty_70_140',
                     '364509':'mmgamma_pty_140_E',
                     '364510':'ttgamma_pty_7_15',
                     '364511':'ttgamma_pty_15_35',
                     '364512':'ttgamma_pty_35_70',
                     '364513':'ttgamma_pty_70_140',
                     '364514':'ttgamma_pty_140_E',
                     '364515':'nngamma_pty_7_15',
                     '364516':'nngamma_pty_15_35',
                     '364517':'nngamma_pty_35_70',
                     '364518':'nngamma_pty_70_140',
                     '364519':'nngamma_pty_140_E',
                 }

    bkg_sherpa_wg = {'364521':'engamma_pty_7_15',
                     '364522':'engamma_pty_15_35',
                     '364523':'engamma_pty_35_70',
                     '364524':'engamma_pty_70_140',
                     '364525':'engamma_pty_140_E',
                     '364526':'mngamma_pty_7_15',
                     '364527':'mngamma_pty_15_35',
                     '364528':'mngamma_pty_35_70',
                     '364529':'mngamma_pty_70_140',
                     '364530':'mngamma_pty_140_E',
                     '364531':'tngamma_pty_7_15',
                     '364532':'tngamma_pty_15_35',
                     '364533':'tngamma_pty_35_70',
                     '364534':'tngamma_pty_70_140',
                     '364535':'tngamma_pty_140_E',
                 }
    bkg_mg_zg = {'345775':'FxFx_eegamma_HT0_125',
                '345776':'FxFx_eegamma_HTGT125_MjjLT150',
                '345777':'FxFx_eegamma_HTGT125_MjjLT500',
                '345778':'FxFx_eegamma_HTGT125_MjjGT500',
                '345779':'FxFx_mumugamma_HT0_125',
                '345780':'FxFx_mumugamma_HTGT125_MjjLT150',
                '345781':'FxFx_mumugamma_HTGT125_MjjLT500',
                '345782':'FxFx_mumugamma_HTGT125_MjjGT500',
                '345784':'FxFx_nunugamma_pty_140',
                         }

    bkg_sherpa_vgg = {'364550':'eegammagamma_pty_17_myy_80',
                      '364552':'eegammagamma_pty_35_70',
                      '364553':'eegammagamma_pty_70_140',
                      '364554':'eegammagamma_pty_140_E_CMS',
                          '364555':'mumugammagamma_pty_17_myy_80',
                          '364557':'mumugammagamma_pty_35_70',
                          '364558':'mumugammagamma_pty_70_140',
                          '364559':'mumugammagamma_pty_140_E_CMS',
                          '364560':'tautaugammagamma_pty_17_myy_80',
                          '364562':'tautaugammagamma_pty_35_70',
                          '364563':'tautaugammagamma_pty_70_140',
                          '364564':'tautaugammagamma_pty_140_E_CMS',
                          '364565':'nunugammagamma_pty_17_myy_80',
                          '364567':'nunugammagamma_pty_35_70',
                          '364568':'nunugammagamma_pty_70_140',
                          '364569':'nunugammagamma_pty_140_E_CMS',
                          '364570':'enugammagamma_pty_17_myy_80',
                          '364572':'enugammagamma_pty_35_70',
                          '364573':'enugammagamma_pty_70_140',
                          '364574':'enugammagamma_pty_140_E_CMS',
                          '364575':'munugammagamma_pty_17_myy_80',
                          '364577':'munugammagamma_pty_35_70',
                          '364578':'munugammagamma_pty_70_140',
                          '364579':'munugammagamma_pty_140_E_CMS',
                          '364580':'taunugammagamma_pty_17_myy_80',
                          '364582':'taunugammagamma_pty_35_70',
                          '364583':'taunugammagamma_pty_70_140',
                          '364584':'taunugammagamma_pty_140_E_CMS',
                          }
    bkg_ttg = {'410082':'ttgamma_noallhad',
                   }
    bkg_pho = {'364541':'SinglePhoton_pty_17_35',
               '364542':'SinglePhoton_pty_35_70',
               '364543':'SinglePhoton_pty_70_140',
               '364544':'SinglePhoton_pty_140_280',
               '364545':'SinglePhoton_pty_280_500',
               '364546':'SinglePhoton_pty_500_1000',
               '364547':'SinglePhoton_pty_1000_E',
           }
    bkg_pho_v2 = {'361040':'SinglePhotonPt35_70_CFilterBVeto',
                  '361041':'SinglePhotonPt35_70_BFilter',
                  '361042':'SinglePhotonPt70_140_CVetoBVeto',
                  '361043':'SinglePhotonPt70_140_CFilterBVeto',
                  '361044':'SinglePhotonPt70_140_BFilter',
                  '361045':'SinglePhotonPt140_280_CVetoBVeto',
                  '361046':'SinglePhotonPt140_280_CFilterBVeto',
                  '361047':'SinglePhotonPt140_280_BFilter',
                  '361048':'SinglePhotonPt280_500_CVetoBVeto',
                  '361049':'SinglePhotonPt280_500_CFilterBVeto',
                  '361050':'SinglePhotonPt280_500_BFilter',
                  '361051':'SinglePhotonPt500_1000_CVetoBVeto',
                  '361052':'SinglePhotonPt500_1000_CFilterBVeto',
                  '361053':'SinglePhotonPt500_1000_BFilter',
                  '361054':'SinglePhotonPt1000_2000_CVetoBVeto',
                  '361055':'SinglePhotonPt1000_2000_CFilterBVeto',
                  '361056':'SinglePhotonPt1000_2000_BFilter',
                  '361057':'SinglePhotonPt2000_4000_CVetoBVeto',
                  '361058':'SinglePhotonPt2000_4000_CFilterBVeto',
                  '361059':'SinglePhotonPt2000_4000_BFilter',
                  '361060':'SinglePhotonPt4000_CVetoBVeto',
                  '361061':'SinglePhotonPt4000_CFilterBVeto',
                  '361062':'SinglePhotonPt4000_BFilter',
                  } #305444
    bkg_Vqq_gamma = {'305435':'WqqGammaPt140_280',
                         '305436':'WqqGammaPt280_500',
                         '305437':'WqqGammaPt500_1000',
                         '305438':'WqqGammaPt1000_2000',
                         '305439':'WqqGammaPt2000_inf',
                         '305440':'ZqqGammaPt140_280',
                         '305441':'ZqqGammaPt280_500',
                         '305442':'ZqqGammaPt500_1000',
                         '305443':'ZqqGammaPt1000_2000',
                         '305444':'ZqqGammaPt2000_inf',
                         }

    if options.mergePTV:
        for ki,yi in bkg_vbfPTVExt.iteritems():
            if yi[0]=='W': bkg_wqcd[ki]=yi
            elif yi[0]=='Z': bkg_zqcd[ki]=yi
    if options.year==2018:
        for ki,yi in bkg_vbfPTVExt.iteritems():
            if yi.count('Znunu'): bkg_zqcd[ki]=yi
    if options.mergeExt:
        for ki,yi in bkg_vbfExt.iteritems():
            if yi[0]=='W': bkg_wqcd[ki]=yi
            elif yi[0]=='Z': bkg_zqcd[ki]=yi


    # add low mass
    bkg_zqcd.update(bkg_lowMassZ)
    #bkg_zqcd.update(bkg_zee_228)
    bkg_keys = {
                'hvh':sig_VH125,
                #'whww':sig_VH125v2,
                'vbfg':sig_vbfgam,
                'whww':alt_VBF,
                'hvbf500':{'308279':'VBF125 - H500',},
                'hvbf1k':{'308281':'VBF125 - H1000',},
                'hvbf3k':{'308283':'VBF125 - H3000',},
                'hggf':sig_ggF125,
                'tth':sig_tth125,
                'hvbf':sig_VBF125,
                'wewk':bkg_wewk,
                #'wewk':bkg_wewkpow,
                'wqcd':bkg_wqcd,
                'zewk':bkg_zewk,
                #'zewk':bkg_zewkpow,
                #'top2':bkg_zewkpow,
                'zqcd':bkg_zqcd,
                'top2':bkg_top2, # all top
                #'top2':bkg_zqcd_sh_ktExtalt, # all top
                #'top2':{'345323':'hww'}, # all top
                #'top2':bkg_zewkpow,
                #'top2':{'312487':'Znunu_PTV100_140_MJJ0_500_KtMerging','312484':'Znunu_PTV100_140_MJJ0_500_KtMerging',}, # all top
                #'top1':bkg_top1,
                ##'hvbf':bkg_wqcd_mnu,
                ##'wewk':bkg_wqcd_tnu,
                ##'wqcd':bkg_wqcd_enu,
                ##'zewk':bkg_zqcd_zmm,
                ##'zqcd':bkg_zqcd_zee,
                ##'top2':bkg_zqcd_ztt,
                ##'top1':bkg_zqcd_znn,
                'vvv':bkg_vv,
                'mqcd':bkg_qcdw,
                'dqcd':bkg_datadriveqcd,
                #'mqcd':bkg_qcdunw,
                'zqcdMad':bkg_z_strong_madgraph,
                'wqcdMad':bkg_w_strong_madgraph,
                'wdpi':bkg_top_other,
                'wgam':bkg_sherpa_wg,
                'zgam':bkg_sherpa_zg,
                'wgamewk':bkg_wgewk,
                'zgamewk':bkg_zgewk,
                'ttg':bkg_ttg,
                'pho':bkg_pho,
                'phoAlt':bkg_pho_v2,
                'vgg':bkg_sherpa_vgg,
                #'zqcdMad':bkg_zqcd,
                #'wqcdMad':bkg_wqcd,
                #'hvbf':bkg_w_strong_madgraph_wmnu,
                #'wewk':bkg_w_strong_madgraph_wenu,
                #'wqcd':bkg_w_strong_madgraph_wtnu,
                #'zewk':bkg_z_strong_madgraph_zmm,
                #'zqcd':bkg_z_strong_madgraph_zee,
                #'top2':bkg_z_strong_madgraph_ztt,
                #'top1':bkg_z_strong_madgraph_znn,
                }

    if not options.mergeKTPTV:
        bkg_keys['wdpi'].update(bkg_zqcd_sh_ktExt)
        bkg_keys['wdpi'].update(bkg_wqcd_sh_ktExt)
    else:
        bkg_keys['zqcd'].update(bkg_zqcd_sh_ktExt)
        bkg_keys['wqcd'].update(bkg_wqcd_sh_ktExt)
    if not options.mergePTV:
        #bkg_keys['wdpi'].update(bkg_zqcd_znn)        
        if  options.year!=2018:
            bkg_keys['wdpi'].update(bkg_vbfPTVExt)
            bkg_keys['wdpi'].update(bkg_zqcd_znn_mc16e)            
        else:
            for ki,yi in bkg_vbfPTVExt.iteritems():
                if not yi.count('Znunu'): bkg_keys['wdpi'][ki]=yi

    if not options.mergeExt:
        bkg_keys['wdpi'].update(bkg_vbfExt)
        bkg_keys['wdpi'].update(bkg_zqcd_LO_Filt)
        bkg_keys['wdpi'].update(bkg_wqcd_LO_Filt)
        bkg_keys['wdpi'].update(bkg_new)

    if not options.mergeMGExt:
        bkg_keys['wdpi'].update(bkg_zqcd_LO_Filt)
        bkg_keys['wdpi'].update(bkg_wqcd_LO_Filt)
    else:
        #bkg_keys['zqcdMad']=bkg_zqcd_LO_Filt
        bkg_keys['zqcdMad'].update(bkg_zqcd_LO_Filt)
        bkg_keys['wqcdMad'].update(bkg_wqcd_LO_Filt)
        #bkg_keys['wdpi'].update(bkg_zqcd_LO_Filt)
        #bkg_keys['wdpi'].update(bkg_z_strong_madgraph)
        #bkg_keys['wdpi'].update(bkg_wqcd_LO_Filt)

    # extra samples here for now
    bkg_keys['wdpi'].update(bkg_wewkpow)
    bkg_keys['wdpi'].update(bkg_zewkpow)
    bkg_keys['wdpi'].update(bkg_zee_228)
    bkg_keys['wdpi'].update(bkg_mg_zg)

    bkg_keys['wdpi'].update({'410083':'ttgamma4080_noallhad','410084':'ttgamma80_noallhad'})
    
    if False:
        bkg_keys['zqcdPow']=bkg_z_strong_powheg
        bkg_keys['vbfz']=bkg_vbfFiltZ
        bkg_keys['zldy']=bkg_lowMassZ
    else:
        #extra_samples=bkg_lowMassZ
        #extra_samples.update(bkg_vbfFiltZ)
        extra_samples=bkg_vbfFiltZ
        extra_samples.update(bkg_z_strong_powheg)
        bkg_keys['wdpi'].update(extra_samples)
        bkg_keys['wdpi'].update(bkg_Vqq_gamma)
    #
    # Select MC samples
    #
    if        keys  == 'all'   : keys = bkg_keys.keys()
    elif type(keys) == type(''): keys = keys.split(',')
    elif type(keys) != type([]): keys = []

    res_keys = {}

    for key in keys:
        if key in bkg_keys:
            for run in bkg_keys[key]:
                res_keys[run] = key
        else:
            log.warning('prepareBkgKeys - unknown key: %s' %key)
            continue

    return res_keys
