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
        
    def __init__(self, alg_name, options, my_files, my_runs_map):
        
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
        self.read_reg.SetVal('ReadEvent::LooseLepZ',     options.LooseLepZ)
        self.read_reg.SetVal('ReadEvent::OverlapPh',     options.OverlapPh)
        self.read_reg.SetVal('ReadEvent::TrigString',    options.trig_name)  # specify a trigger from the command line       
            
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
        inp_vars = get_vars.GetVarStr(0)
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
        
    sig_VH125     = {'308072':'VH125',
                         '308071':'VH125',
                         }
    sig_ggF125 = {'308284':'ggF125',}
    #sig_ggF125 = {'364162':'Wmunu_MAXHTPTV140_280_CVetoBVeto',}
    #sig_VH125     = {'364106':'TBD',}
    #sig_VH125v2     = {'364148':'TBD',}    
    sig_VBF125     = {'308276':'VBF125 - met',
                      '308567':'VBF125 - all',                                                                                        
                          }
    alt_VBF = {'308275':'VBF125 - H75',
                      '308277':'VBF125 - H200',
                      '308278':'VBF125 - H300',                                                                  
                      '308279':'VBF125 - H500',                                                                  
                      '308280':'VBF125 - H750',                                                                  
                      '308281':'VBF125 - H1000',                                                                  
                      '308282':'VBF125 - H2000',                                                                  
                      '308283':'VBF125 - H3000',}

    bkg_wewk =     {'308096':'TBD',
                    '308097':'TBD',
                    '308098':'TBD',
                    '363359':'TBD',
                    '363360':'TBD',
                    '363489':'TBD',
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
    bkg_zewk =     {'308092':'TBD',
                    '308093':'TBD',                        
                    '308094':'TBD',
                    '308095':'TBD',                        
                    '363355':'TBD',                        
                    '363356':'TBD',                        
                    '363357':'TBD',                        
                    '363358':'TBD',                        
                        }
    
    bkg_zqcd_zmm = {'364100':'Zmumu_MAXHTPTV0_70_CVetoBVeto',
                    '364101':'TBD',
                    '364102':'TBD',
                    '364103':'TBD',
                    '364104':'TBD',
                    '364105':'TBD',
                    '364106':'TBD',
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
                    '364117':'TBD',
                    '364118':'TBD',
                    '364119':'TBD',
                    '364120':'TBD',
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
                    '364131':'TBD',
                    '364132':'TBD',
                    '364133':'TBD',
                    '364134':'TBD',
                    '364135':'TBD',
                    '364136':'TBD',
                    '364137':'TBD',
                    '364138':'TBD',
                    '364139':'TBD',
                    '364140':'TBD',
                    '364141':'TBD',}
    bkg_zqcd_znn = {'364142':'Znunu_MAXHTPTV0_70_CVetoBVeto',
                    '364143':'TBD',
                    '364144':'TBD',
                    '364145':'TBD',
                    '364146':'TBD',
                    '364147':'TBD',
                    '364148':'TBD',
                    '364149':'TBD',
                    '364150':'TBD',
                    '364151':'TBD',
                    '364152':'TBD',
                    '364153':'TBD',
                    '364154':'TBD',
                    '364155':'Znunu_MAXHTPTV1000',
                    }
    bkg_zqcd={}
    bkg_zqcd.update(bkg_zqcd_zmm)
    bkg_zqcd.update(bkg_zqcd_zee)
    bkg_zqcd.update(bkg_zqcd_ztt)
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
        '410472':'ttbar(w/dil)',                
        }
    bkg_top1 = {
        '410011':'tchan_top',
        '410012':'tchan_antitop',
        '410013':'Wt_top',
        '410014':'Wt_top',
        '410025':'schan_top',
        '410026':'schan_antitop',
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
                  '363494':'vvvv',                  
                  '364250':'llll',                  
                  '364254':'llvv',                  
                  '364255':'lvvv',                  
                  }
    bkg_vbfFiltZ = {'345099':'TBD',
                        '345100':'TBD',
                        '345101':'TBD',
                        '345102':'TBD',
                        }
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

    bkg_keys = {
                'hvh':sig_VH125,
                #'whww':sig_VH125v2,
                'whww':alt_VBF,
                'hggf':sig_ggF125,
                'hvbf':sig_VBF125,
                'wewk':bkg_wewk,
                'wqcd':bkg_wqcd,
                'zewk':bkg_zewk,
                'zqcd':bkg_zqcd,
                'top2':bkg_top2,
                'top1':bkg_top1,
                ##'hvbf':bkg_wqcd_mnu,
                ##'wewk':bkg_wqcd_tnu,
                ##'wqcd':bkg_wqcd_enu,
                ##'zewk':bkg_zqcd_zmm,
                ##'zqcd':bkg_zqcd_zee,
                ##'top2':bkg_zqcd_ztt,
                ##'top1':bkg_zqcd_znn,
                'zldy':bkg_lowMassZ,                
                'vvv':bkg_vv,
                'dqcd':bkg_qcdw,
                'mqcd':bkg_qcdunw,
                'vbfz':bkg_vbfFiltZ,
                'zqcdMad':bkg_z_strong_madgraph,
                'wqcdMad':bkg_w_strong_madgraph,
                #'zqcdMad':bkg_zqcd,
                #'wqcdMad':bkg_wqcd,
                'zqcdPow':bkg_z_strong_powheg,

                #'hvbf':bkg_w_strong_madgraph_wmnu,
                #'wewk':bkg_w_strong_madgraph_wenu,
                #'wqcd':bkg_w_strong_madgraph_wtnu,
                #'zewk':bkg_z_strong_madgraph_zmm,
                #'zqcd':bkg_z_strong_madgraph_zee,
                #'top2':bkg_z_strong_madgraph_ztt,
                #'top1':bkg_z_strong_madgraph_znn,                
                }

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
