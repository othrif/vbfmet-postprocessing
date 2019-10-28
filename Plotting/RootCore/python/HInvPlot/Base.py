
import os
import sys
#import PyCintex,
import ROOT

import HInvPlot.JobOptions as config

log = config.getLog('Base.py')
            
#-------------------------------------------------------------------------
class ExecBase:
    """ExecBase - python wrapper for C++ algorithms inherting from IExecAlg"""
        
    def __init__(self,
                 alg_name,
                 alg_type,
                 alg_inst,
                 reg_inst):
                     
        if not hasattr(alg_inst, 'DoConf'):
            log.error('ExecBase - wrong algorithm instance for %s' %alg_name)
            sys.exit(1)

        if not hasattr(reg_inst, 'KeyExists'):
            log.error('ExecBase - wrong registry instance for %s' %alg_name)
            sys.exit(1)
        
        self.alg_name     = alg_name
        self.alg_type     = alg_type
        self.sub_algs     = []
        
        self.plot_reg     = reg_inst
        self.plot_alg     = alg_inst

        #
        # Set algorithm name/type and store Registry for later configuration
        #
        self.plot_alg.SetName(alg_name)
        self.plot_alg.SetType(alg_type)

        self.plot_alg.SetAlgConf(self.plot_reg)
        
    def DoConf(self):
        self.plot_alg.DoConf(self.plot_reg)

    def DoSave(self, dir):
        self.plot_alg.DoSave(dir)

    def GetCppExecAlg(self):
        return self.plot_alg

    def AddSubAlg(self, alg):
        if type(alg) == type([]):
            self.sub_algs +=  alg
        else:
            self.sub_algs += [alg]
            
    def GetName(self):
        return self.alg_name

    def GetType(self):
        return self.alg_type

    def ConvertAlgToList(self, alg):
        if alg == None or (type(alg) == type([]) and len(alg) == 0):
            return None
        
        if type(alg) != type([]):
            alg = [alg]

        res = []
            
        for a in alg:
            if hasattr(a, 'GetCppExecAlg'):
               res += [a]
            else:
                raise TypeError('ConvertAlgToList - invalid type: %s' %type(a))

        return res

    def SetPassAlg(self, alg):
        algs = self.ConvertAlgToList(alg)

        if algs == None:
            return
        elif len(algs) != 1:
            raise TypeError('SetPassAlg - invalid alg: %s' %type(alg))
        
        for a in algs:
            self.GetCppExecAlg().SetPassAlg(a.GetCppExecAlg())
            self.sub_algs += [a]

#-------------------------------------------------------------------------
class CutItem:
    """CutItem - python wrapper for C++ CutItem class"""
        
    def __init__(self, name, conf='', weight=None):

        self.cut_name = name
        self.cut_conf = conf
        self.cut_wkey = weight
        self.cut_reg  = ROOT.Msl.Registry()
        self.list_and = []
        self.list_or  = []

        if not self.IsValidConf(conf):
            pass

        self.cut_reg.SetVal('CutName', name)
        self.cut_reg.SetVal('CutConf', conf)
        
        if type(self.cut_wkey) == type(''):
            self.cut_reg.SetVal('CutWeightKey', self.cut_wkey)
        elif type(self.cut_wkey) == type([]):
            self.cut_reg.SetVal('CutWeightKey', ','.join(self.cut_wkey))
        
    def IsValidConf(self, conf):
        if type(conf) != type(''):
            raise NameError('CutItem::IsValidConf - invalid input type: %s' %conf)

        #
        # Lists of known variables (Msl::Mva::Var enum from Event.h) and operators
        #        
        vars = ROOT.Msl.Mva.GetAllVarNames()
        oprs = ['>=', '>', '<=', '<', '==']

        #
        # Split using logical AND=&& or OR==|| and check that expressions are valid
        #
        if conf.count('&&') and conf.count('||'):
            log.error('CutItem - conf="%s" can not contain both && and || operators' %conf)
            sys.exit(1)
        elif conf.count('||'):
            confs = conf.split('||')
        else:
            confs = conf.split('&&')

        for v in confs:
            if len(v) == 0:
                continue

            for o in oprs:
                if v.find(o) > 0:
                    break
                o = None
                
            if o == None:
                raise NameError('CutItem::IsValidConf - "%s" does not contain known operator' %conf)

            parts = v.split(o)

            if len(parts) != 2:
                log.error('CutItem - conf="%s" has invalid logic %s: %s, %s' %(conf, v, o, parts))
                sys.exit(1)

            var_name = parts[0]
            var_comp = parts[1]

            if var_name.strip() not in vars:
                log.error('CutItem - conf="%s" does not contain known variable: %s' %(conf, var_name))
                sys.exit(1)                
            
            try:
                var_comp = float(var_comp)
            except ValueError:
                log.error('CutItem - conf="%s" contains comparison with non-number' %conf)
                sys.exit(1)
                
            #
            # Logical expression is valid and contains only known variables
            #
            log.debug('CutItem - conf="%s": %s %s %f' %(conf, var_name, o, var_comp))

        #
        # Check that weight key is valid
        #
        if type(self.cut_wkey) == type('') and self.cut_wkey not in vars:
            log.error('CutItem - unknown weight key: %s' %self.cut_wkey)
            sys.exit(1)            

        return True

    def GetRegistry(self):
        return self.cut_reg

    def GetCutName(self):
        return self.cut_name

    def AddCut(self, cut, option):

        if cut.GetCutName() in self.list_and + self.list_or:
            log.warning('AddCut - duplicate cut: %s' %cut.GetCutName())
            return False
            
        if   option.lower() == 'and': self.list_and += [cut.GetCutName()]
        elif option.lower() == 'or' : self.list_or  += [cut.GetCutName()]
        else: 
            log.warning('AddCut - unknown option %s: %s' %(cut.GetCutName(), option))

        self.cut_reg.SetVal(cut.GetCutName(), cut.GetRegistry())
        self.cut_reg.SetVal('ListAND',        ','.join(self.list_and))
        self.cut_reg.SetVal('ListOR',         ','.join(self.list_or))

        return True
        

#-----------------------------------------------------------------------------------------------------        
def PrepareJobDescPenn(options,script='macros/plotEvent.py',runFileName='plotEvent'):
    
    if options.output == None:
        log.error('Need output option')
        sys.exit(1)

    #
    # Prepare condor submission file
    #
    testArea = os.environ.get('ROOTCOREDIR').rstrip('/')+'/..'
    studyJob = '%s/HInvPlot/%s' %(testArea,script)
    
    jobPath  = '%s'               %options.output.rstrip('/')
    jobFile  = '%s/%s.run'        %(jobPath,runFileName)
    
    jobDesc  = ''
    jobDesc += 'universe                = vanilla\n'
    jobDesc += 'getenv                  = True\n'
    jobDesc += 'should_transfer_files   = YES\n'
    jobDesc += 'when_to_transfer_output = ON_EXIT_OR_EVICT\n'
    jobDesc += 'executable              = %s\n'        %studyJob
    jobDesc += '\n'

    return  jobDesc,jobPath,jobFile

#-----------------------------------------------------------------------------------------------------        
def makeJobOptions(options, jobOpts, jobDir=None, jobKey='job'):
    
    #
    # Build arguments for one job
    #
    jobDesc  = ''
    jobDesc += 'output     = %s.stdout\n' %jobKey
    jobDesc += 'error      = %s.stderr\n' %jobKey

    if jobDir != None:
        jobPath = '%s/%s' %(options.output.rstrip('/'), jobDir)
        jobDesc += 'initialdir = %s\n' %jobPath

        try:
            os.makedirs(jobPath)
        except OSError:

            if os.path.isdir(jobPath):
                if options.overwrite:
                    pass
                else:
                    log.error('makeJobOptions - path exists: %s' %jobPath)
                    sys.exit(1)       
            else:
                log.error('makeJobOptions - failed to mkdir: %s' %jobPath)
                sys.exit(1)

    jobDesc += 'arguments  = "%s"\n' %jobOpts
    jobDesc += 'queue\n\n'            
    
    return jobDesc

#-----------------------------------------------------------------------------------------------------        
def SubmitBatch(options,jobFile,jobPath,jobDesc,log,ijob):

    from subprocess import Popen, PIPE

    if os.path.isfile(jobFile) and not options.overwrite:
        log.warning('Job file already exists: %s' %jobFile)
        sys.exit(1)

    if ijob == 0:
        log.warning('No jobs configured - nothing to do')
        sys.exit(0)

    if not os.path.isdir(jobPath):
        os.makedirs(jobPath)

    pfile = open(jobFile, 'w')
    pfile.write(jobDesc)
    pfile.close()

    if not options.submit_penn:
        elist = ['cat', jobFile]
    else:
        elist = ['condor_submit', jobFile]
    
    
    log.info('Execute command: %s' %str(elist))

    output = Popen(elist, stdout=PIPE, stderr=PIPE).communicate()

    log.info('-----------------------------------------------------')
    for line in output:
        print line
    log.info('-----------------------------------------------------')
