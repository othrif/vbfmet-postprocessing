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
        syst_class = systematics.systematics(None)
        self.read_reg.SetVal('ReadEvent::SystList',','.join(syst_class.getsystematicsList()))
        
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

    def Save(self, rfile, dirname = None):
        if type(rfile) != type(''):
            self.read_alg.Save(0)
            return

        rfile = ROOT.TFile(rfile, 'RECREATE')

        log.info('ReadEvent - save algorithms...')

        if type(dirname) == type(''):
            self.read_alg.Save(rfile.mkdir('%s' %(dirname)))
        else:
            self.read_alg.Save(rfile)

        log.info('ReadEvent - write file...')

        rfile.Write()
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

    sig_ggF125 = {'308284':'ggF125',}    
    sig_VBF125     = {'308276':'VBF125 - met',
                      '308567':'VBF125 - all',
                          }
    sig_VH125     = {'308072':'VH125',}
    bkg_wewk =     {'308096':'TBD',                        
                    '308097':'TBD',                        
                    '308098':'TBD',                        
                    '363359':'TBD',                        
                    '363360':'TBD',                        
                    '363489':'TBD',                        
                        }
    bkg_wqcd =     {'364156':'TBD',
                    '364157':'TBD',
                    '364158':'TBD',
                    '364159':'TBD',
                    '364160':'TBD',
                    '364161':'TBD',
                    '364162':'TBD',
                    '364163':'TBD',
                    '364164':'TBD',
                    '364165':'TBD',
                    '364166':'TBD',
                    '364167':'TBD',
                    '364168':'TBD',
                    '364169':'TBD',
                    '364170':'TBD',
                    '364171':'TBD',
                    '364172':'TBD',
                    '364173':'TBD',
                    '364174':'TBD',
                    '364175':'TBD',
                    '364176':'TBD',
                    '364177':'TBD',
                    '364178':'TBD',
                    '364179':'TBD',
                    '364180':'TBD',
                    '364181':'TBD',
                    '364182':'TBD',
                    '364183':'TBD',
                    '364184':'TBD',
                    '364185':'TBD',
                    '364186':'TBD',
                    '364187':'TBD',
                    '364188':'TBD',
                    '364189':'TBD',
                    '364190':'TBD',
                    '364191':'TBD',
                    '364192':'TBD',
                    '364193':'TBD',
                    '364194':'TBD',
                    '364195':'TBD',
                    '364196':'TBD',
                    '364197':'TBD',
                        }
    bkg_zewk =     {'308092':'TBD',
                    '308093':'TBD',                        
                    '308094':'TBD',                        
                    '308095':'TBD',                        
                    '363355':'TBD',                        
                    '363356':'TBD',                        
                    '363357':'TBD',                        
                    '363358':'TBD',                        
                        }
    
    bkg_zqcd =     {'364100':'TBD',
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
                    '364113':'TBD',
                    '364114':'TBD',
                    '364115':'TBD',
                    '364116':'TBD',
                    '364117':'TBD',
                    '364118':'TBD',
                    '364119':'TBD',
                    '364120':'TBD',
                    '364121':'TBD',
                    '364122':'TBD',
                    '364123':'TBD',
                    '364124':'TBD',
                    '364125':'TBD',
                    '364126':'TBD',
                    '364127':'TBD',
                    '364128':'TBD',
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
                    '364141':'TBD',
                    '364142':'TBD',
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
                    '364155':'TBD',
                    }
    
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
        }
    bkg_top1 = {
        '410011':'tchan_top',
        '410012':'tchan_antitop',
        '410013':'Wt_top',
        '410014':'Wt_top',
        '410025':'schan_top',
        '410026':'schan_antitop',
        }

    bkg_keys = {
                'hvh':sig_VH125,                
                'hggf':sig_ggF125,                
                'hvbf':sig_VBF125,                
                'wewk':bkg_wewk,                
                'wqcd':bkg_wqcd,
                'zewk':bkg_zewk,                
                'zqcd':bkg_zqcd,                                
                'top2':bkg_top2,
                'top1':bkg_top1,
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
