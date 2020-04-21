import math
import ROOT

class HistEntry:
    def __init__(self, hist, hname, file):
        self.hname    = hname
        self.hist     = hist.Clone()
        self.file     = file
    def merge_bins(self):
        self.hist.SetBinContent(1,self.hist.GetBinContent(0)+self.hist.GetBinContent(1))
        self.hist.SetBinError(1,math.sqrt(self.hist.GetBinError(0)**2+self.hist.GetBinError(1)**2))
        self.hist.SetBinContent(0,0)
        self.hist.SetBinError(0,0)
        last_bin=self.hist.GetNbinsX()
        #print 'last_bin: ',last_bin,' ',self.hist.GetNbinsX()
        my_err = ROOT.Double(0)
        my_last_bin_val = self.hist.IntegralAndError(last_bin,self.hist.GetNbinsX()+5, my_err)
        self.hist.SetBinContent(last_bin,my_last_bin_val)
        self.hist.SetBinError(last_bin,my_err)
        for mbin in range(last_bin+1,self.hist.GetNbinsX()+2):
            self.hist.SetBinContent(mbin,0.0)
            self.hist.SetBinError(mbin,0.0)
        return self.hist

    def walk(self,
             top=None,
             path=None,
             depth=0,
             maxdepth=-1,
             class_ref=None,
             class_pattern=None,
             return_classname=False,
             treat_dirs_as_objs=False):
        dirnames, objectnames = [], []
        tdirectory = self.GetDirectory(top) if top else self
        for key in tdirectory.keys(latest=True):
            name = key.GetName()
            classname = key.GetClassName()
            is_directory = classname.startswith('TDirectory')
            if is_directory:
                dirnames.append(name)
            if not is_directory or treat_dirs_as_objs:
                if class_ref is not None:
                    tclass = ROOT.TClass.GetClass(classname, True, True)
                    if not tclass or not tclass.InheritsFrom(class_ref.Class()):
                        continue
                if class_pattern is not None:
                    if not fnmatch(classname, class_pattern):
                        continue
                name = (name if not return_classname else (name, classname))
                objectnames.append(name)
        if path:
            dirpath = os.path.join(path, tdirectory.GetName())
        elif not isinstance(tdirectory, ROOT.R.TFile):
            dirpath = tdirectory.GetName()
        else:
            dirpath = ''
        yield dirpath, dirnames, objectnames
        if depth == maxdepth:
            return
        for dirname in dirnames:
            rdir = tdirectory.GetDirectory(dirname)
            for x in rdir.walk(
                    class_ref=class_ref,
                    class_pattern=class_pattern,
                    depth=depth + 1,
                    maxdepth=maxdepth,
                    path=dirpath,
                    return_classname=return_classname,
                    treat_dirs_as_objs=treat_dirs_as_objs):
                yield x
    def GetDirectory(self, path, rootpy=True, **kwargs):
        rdir = super(_DirectoryBase, self).GetDirectory(path)
        if not rdir:
            raise DoesNotExist
        if rootpy:
            return asrootpy(rdir, **kwargs)
        return rdir
