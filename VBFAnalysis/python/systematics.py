class systematics(object):
    def __init__(self,mode):
        self.systematicsList=""
        self.load(mode)
        self.removeList=['TAUS_','PH_','JET_MassRes_','JET_Rtrk_']
    def load(self,mode="All"):
        self.removeList=['TAUS_','PH_','JET_MassRes_','JET_Rtrk_']
        if mode == "All":
            self.systematicsList = ['Nominal', 'EG_RESOLUTION_ALL__1down', 'EG_RESOLUTION_ALL__1up', 'EG_SCALE_AF2__1down', 'EG_SCALE_AF2__1up', 'EG_SCALE_ALL__1down', 'EG_SCALE_ALL__1up', 'JET_Comb_Baseline_Kin__1down', 'JET_Comb_Baseline_Kin__1up', 'JET_Comb_Modelling_Kin__1down', 'JET_Comb_Modelling_Kin__1up', 'JET_Comb_TotalStat_Kin__1down', 'JET_Comb_TotalStat_Kin__1up', 'JET_Comb_Tracking_Kin__1down', 'JET_Comb_Tracking_Kin__1up', 'JET_EtaIntercalibration_NonClosure_highE__1down', 'JET_EtaIntercalibration_NonClosure_highE__1up', 'JET_EtaIntercalibration_NonClosure_negEta__1down', 'JET_EtaIntercalibration_NonClosure_negEta__1up', 'JET_EtaIntercalibration_NonClosure_posEta__1down', 'JET_EtaIntercalibration_NonClosure_posEta__1up', 'JET_Flavor_Response__1down', 'JET_Flavor_Response__1up', 'JET_GroupedNP_1__1down', 'JET_GroupedNP_1__1up', 'JET_GroupedNP_2__1down', 'JET_GroupedNP_2__1up', 'JET_GroupedNP_3__1down', 'JET_GroupedNP_3__1up', 'JET_JER_DataVsMC__1down', 'JET_JER_DataVsMC__1up', 'JET_JER_EffectiveNP_1__1down', 'JET_JER_EffectiveNP_1__1up', 'JET_JER_EffectiveNP_2__1down', 'JET_JER_EffectiveNP_2__1up', 'JET_JER_EffectiveNP_3__1down', 'JET_JER_EffectiveNP_3__1up', 'JET_JER_EffectiveNP_4__1down', 'JET_JER_EffectiveNP_4__1up', 'JET_JER_EffectiveNP_5__1down', 'JET_JER_EffectiveNP_5__1up', 'JET_JER_EffectiveNP_6__1down', 'JET_JER_EffectiveNP_6__1up', 'JET_JER_EffectiveNP_7restTerm__1down', 'JET_JER_EffectiveNP_7restTerm__1up', 'JET_MassRes_Hbb__1down', 'JET_MassRes_Hbb__1up', 'JET_MassRes_Top__1down', 'JET_MassRes_Top__1up', 'JET_MassRes_WZ__1down', 'JET_MassRes_WZ__1up', 'JET_Rtrk_Baseline_Sub__1down', 'JET_Rtrk_Baseline_Sub__1up', 'JET_Rtrk_Modelling_Sub__1down', 'JET_Rtrk_Modelling_Sub__1up', 'JET_Rtrk_TotalStat_Sub__1down', 'JET_Rtrk_TotalStat_Sub__1up', 'JET_Rtrk_Tracking_Sub__1down', 'JET_Rtrk_Tracking_Sub__1up', 'MET_SoftTrk_ResoPara', 'MET_SoftTrk_ResoPerp', 'MET_SoftTrk_ScaleDown', 'MET_SoftTrk_ScaleUp', 'MUON_ID__1down', 'MUON_ID__1up', 'MUON_MS__1down', 'MUON_MS__1up', 'MUON_SAGITTA_RESBIAS__1down', 'MUON_SAGITTA_RESBIAS__1up', 'MUON_SAGITTA_RHO__1down', 'MUON_SAGITTA_RHO__1up', 'MUON_SCALE__1down', 'MUON_SCALE__1up', 'FT_EFF_B_systematics__1down', 'FT_EFF_B_systematics__1up', 'FT_EFF_C_systematics__1down', 'FT_EFF_C_systematics__1up', 'FT_EFF_Light_systematics__1down', 'FT_EFF_Light_systematics__1up', 'FT_EFF_extrapolation__1down', 'FT_EFF_extrapolation__1up', 'FT_EFF_extrapolation_from_charm__1down', 'FT_EFF_extrapolation_from_charm__1up', 'EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'eleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'eleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'JET_fJvtEfficiency__1down', 'JET_fJvtEfficiency__1up', 'JET_JvtEfficiency__1down', 'JET_JvtEfficiency__1up', 'MUON_EFF_TrigStatUncertainty__1down', 'MUON_EFF_TrigStatUncertainty__1up', 'MUON_EFF_TrigSystUncertainty__1down', 'MUON_EFF_TrigSystUncertainty__1up', 'MUON_EFF_BADMUON_STAT__1down', 'MUON_EFF_BADMUON_STAT__1up', 'MUON_EFF_BADMUON_SYS__1down', 'MUON_EFF_BADMUON_SYS__1up', 'MUON_EFF_ISO_STAT__1down', 'MUON_EFF_ISO_STAT__1up', 'MUON_EFF_ISO_SYS__1down', 'MUON_EFF_ISO_SYS__1up', 'MUON_EFF_RECO_STAT_LOWPT__1down', 'MUON_EFF_RECO_STAT_LOWPT__1up', 'MUON_EFF_RECO_STAT__1down', 'MUON_EFF_RECO_STAT__1up', 'MUON_EFF_RECO_SYS_LOWPT__1down', 'MUON_EFF_RECO_SYS_LOWPT__1up', 'MUON_EFF_RECO_SYS__1down', 'MUON_EFF_RECO_SYS__1up', 'MUON_EFF_TTVA_STAT__1down', 'MUON_EFF_TTVA_STAT__1up', 'MUON_EFF_TTVA_SYS__1down', 'MUON_EFF_TTVA_SYS__1up', 'PRW_DATASF__1down', 'PRW_DATASF__1up']
#            self.systematicsList = ['Nominal', 'EG_RESOLUTION_ALL__1down', 'EG_RESOLUTION_ALL__1up', 'EG_SCALE_AF2__1down', 'EG_SCALE_AF2__1up', 'EG_SCALE_ALL__1down', 'EG_SCALE_ALL__1up', 'EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down', 'EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up', 'FT_EFF_B_systematics__1down', 'FT_EFF_B_systematics__1up', 'FT_EFF_C_systematics__1down', 'FT_EFF_C_systematics__1up', 'FT_EFF_Light_systematics__1down', 'FT_EFF_Light_systematics__1up', 'FT_EFF_extrapolation__1down', 'FT_EFF_extrapolation__1up', 'FT_EFF_extrapolation_from_charm__1down', 'FT_EFF_extrapolation_from_charm__1up', 'JET_Comb_Baseline_Kin__1up', 'JET_Comb_Baseline_Kin__1down', 'JET_Comb_Modelling_Kin__1up', 'JET_Comb_Modelling_Kin__1down', 'JET_Comb_TotalStat_Kin__1up', 'JET_Comb_TotalStat_Kin__1down', 'JET_Comb_Tracking_Kin__1up', 'JET_Comb_Tracking_Kin__1down', 'JET_EtaIntercalibration_NonClosure__1up', 'JET_EtaIntercalibration_NonClosure__1down', 'JET_GroupedNP_1__1up', 'JET_GroupedNP_1__1down', 'JET_GroupedNP_2__1up', 'JET_GroupedNP_2__1down', 'JET_GroupedNP_3__1up', 'JET_GroupedNP_3__1down', 'JET_JER_SINGLE_NP__1up', 'JET_JvtEfficiency__1down', 'JET_JvtEfficiency__1up', 'JET_MassRes_Hbb__1up', 'JET_MassRes_Hbb__1down', 'JET_MassRes_Top__1up', 'JET_MassRes_Top__1down', 'JET_MassRes_WZ__1up', 'JET_MassRes_WZ__1down', 'JET_Rtrk_Baseline_Sub__1up', 'JET_Rtrk_Baseline_Sub__1down', 'JET_Rtrk_Modelling_Sub__1up', 'JET_Rtrk_Modelling_Sub__1down', 'JET_Rtrk_TotalStat_Sub__1up', 'JET_Rtrk_TotalStat_Sub__1down', 'JET_Rtrk_Tracking_Sub__1up', 'JET_Rtrk_Tracking_Sub__1down', 'JET_fJvtEfficiency__1down', 'JET_fJvtEfficiency__1up', 'MET_SoftTrk_ResoPara', 'MET_SoftTrk_ResoPerp', 'MET_SoftTrk_ScaleDown', 'MET_SoftTrk_ScaleUp', 'MUON_EFF_BADMUON_STAT__1down', 'MUON_EFF_BADMUON_STAT__1up', 'MUON_EFF_BADMUON_SYS__1down', 'MUON_EFF_BADMUON_SYS__1up', 'MUON_EFF_ISO_STAT__1down', 'MUON_EFF_ISO_STAT__1up', 'MUON_EFF_ISO_SYS__1down', 'MUON_EFF_ISO_SYS__1up', 'MUON_EFF_RECO_STAT__1down', 'MUON_EFF_RECO_STAT__1up', 'MUON_EFF_RECO_STAT_LOWPT__1down', 'MUON_EFF_RECO_STAT_LOWPT__1up', 'MUON_EFF_RECO_SYS__1down', 'MUON_EFF_RECO_SYS__1up', 'MUON_EFF_RECO_SYS_LOWPT__1down', 'MUON_EFF_RECO_SYS_LOWPT__1up', 'MUON_EFF_TTVA_STAT__1down', 'MUON_EFF_TTVA_STAT__1up', 'MUON_EFF_TTVA_SYS__1down', 'MUON_EFF_TTVA_SYS__1up', 'MUON_EFF_TrigStatUncertainty__1down', 'MUON_EFF_TrigStatUncertainty__1up', 'MUON_EFF_TrigSystUncertainty__1down', 'MUON_EFF_TrigSystUncertainty__1up', 'MUON_ID__1down', 'MUON_ID__1up', 'MUON_MS__1down', 'MUON_MS__1up', 'MUON_SAGITTA_RESBIAS__1down', 'MUON_SAGITTA_RESBIAS__1up', 'MUON_SAGITTA_RHO__1down', 'MUON_SAGITTA_RHO__1up', 'MUON_SCALE__1down', 'MUON_SCALE__1up', 'PH_EFF_ID_Uncertainty__1down', 'PH_EFF_ID_Uncertainty__1up', 'PH_EFF_ISO_Uncertainty__1down', 'PH_EFF_ISO_Uncertainty__1up', 'PH_EFF_TRIGGER_Uncertainty__1down', 'PH_EFF_TRIGGER_Uncertainty__1up', 'PRW_DATASF__1down', 'PRW_DATASF__1up', 'TAUS_TRUEELECTRON_EFF_ELEOLR_TOTAL__1down', 'TAUS_TRUEELECTRON_EFF_ELEOLR_TOTAL__1up', 'TAUS_TRUEHADTAU_EFF_ELEOLR_TOTAL__1down', 'TAUS_TRUEHADTAU_EFF_ELEOLR_TOTAL__1up', 'TAUS_TRUEHADTAU_EFF_JETID_HIGHPT__1down', 'TAUS_TRUEHADTAU_EFF_JETID_HIGHPT__1up', 'TAUS_TRUEHADTAU_EFF_JETID_TOTAL__1down', 'TAUS_TRUEHADTAU_EFF_JETID_TOTAL__1up', 'TAUS_TRUEHADTAU_EFF_RECO_HIGHPT__1down', 'TAUS_TRUEHADTAU_EFF_RECO_HIGHPT__1up', 'TAUS_TRUEHADTAU_EFF_RECO_TOTAL__1down', 'TAUS_TRUEHADTAU_EFF_RECO_TOTAL__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2015__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2015__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2016__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2016__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2017__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATDATA2017__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2015__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2015__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2016__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2016__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2017__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_STATMC2017__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2015__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2015__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2016__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2016__1up', 'TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2017__1down', 'TAUS_TRUEHADTAU_EFF_TRIGGER_SYST2017__1up', 'TAUS_TRUEHADTAU_SME_TES_DETECTOR__1down', 'TAUS_TRUEHADTAU_SME_TES_DETECTOR__1up', 'TAUS_TRUEHADTAU_SME_TES_INSITU__1down', 'TAUS_TRUEHADTAU_SME_TES_INSITU__1up', 'TAUS_TRUEHADTAU_SME_TES_MODEL__1down', 'TAUS_TRUEHADTAU_SME_TES_MODEL__1up']

            # Filter out the unwanted systematics 
            systematicsList_tmp = []
            for s in self.systematicsList:
                filtFound=False
                for filt in self.removeList:
                    if s.find(filt)>-0.5:
                        print 'Systematic was filtered out: ',s
                        filtFound=True
                        break
                if not filtFound:
                    systematicsList_tmp+=[s]
            self.systematicsList = systematicsList_tmp

        elif mode == "Nominal":
            self.systematicsList = ["Nominal"]
        elif mode == "WeightSyst":
            self.systematicsList = ['FT_EFF_B_systematics__1down','FT_EFF_B_systematics__1up','FT_EFF_C_systematics__1down','FT_EFF_C_systematics__1up','FT_EFF_Light_systematics__1down','FT_EFF_Light_systematics__1up','FT_EFF_extrapolation__1down','FT_EFF_extrapolation__1up','FT_EFF_extrapolation_from_charm__1down','FT_EFF_extrapolation_from_charm__1up','EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_TriggerEff_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ChargeIDSel_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down','EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down','eleANTISFEL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up','eleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down','eleANTISFEL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up','JET_fJvtEfficiency__1down','JET_fJvtEfficiency__1up','JET_JvtEfficiency__1down','JET_JvtEfficiency__1up','MUON_EFF_TrigStatUncertainty__1down','MUON_EFF_TrigStatUncertainty__1up','MUON_EFF_TrigSystUncertainty__1down','MUON_EFF_TrigSystUncertainty__1up','MUON_EFF_BADMUON_STAT__1down','MUON_EFF_BADMUON_STAT__1up','MUON_EFF_BADMUON_SYS__1down','MUON_EFF_BADMUON_SYS__1up','MUON_EFF_ISO_STAT__1down','MUON_EFF_ISO_STAT__1up','MUON_EFF_ISO_SYS__1down','MUON_EFF_ISO_SYS__1up','MUON_EFF_RECO_STAT_LOWPT__1down','MUON_EFF_RECO_STAT_LOWPT__1up','MUON_EFF_RECO_STAT__1down','MUON_EFF_RECO_STAT__1up','MUON_EFF_RECO_SYS_LOWPT__1down','MUON_EFF_RECO_SYS_LOWPT__1up','MUON_EFF_RECO_SYS__1down','MUON_EFF_RECO_SYS__1up','MUON_EFF_TTVA_STAT__1down','MUON_EFF_TTVA_STAT__1up','MUON_EFF_TTVA_SYS__1down','MUON_EFF_TTVA_SYS__1up','PRW_DATASF__1down','PRW_DATASF__1up',]
        elif mode == "Electrons":
            self.systematicsList = ["Nominal", "EG_RESOLUTION_ALL__1down", "EG_RESOLUTION_ALL__1up", "EG_SCALE_ALL__1down", "EG_SCALE_ALL__1up", "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_ID_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1down",  "EL_EFF_Iso_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_Reco_TOTAL_1NPCOR_PLUS_UNCOR__1up", "EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1down", "EL_EFF_Trigger_TOTAL_1NPCOR_PLUS_UNCOR__1up"]
        elif mode == "Muons":
            self.systematicsList = ["MUON_EFF_STAT__1down", "MUON_EFF_STAT__1up", "MUON_EFF_SYS__1down", "MUON_EFF_SYS__1up", "MUON_EFF_TrigStatUncertainty__1down", "MUON_EFF_TrigStatUncertainty__1up", "MUON_EFF_TrigSystUncertainty__1down", "MUON_EFF_TrigSystUncertainty__1up", "MUON_ID__1down", "MUON_ID__1up", "MUON_ISO_STAT__1down", "MUON_ISO_STAT__1up", "MUON_ISO_SYS__1down", "MUON_ISO_SYS__1up", "MUON_MS__1down", "MUON_MS__1up", "MUON_SAGITTA_RESBIAS__1down", "MUON_SAGITTA_RESBIAS__1up", "MUON_SAGITTA_RHO__1down", "MUON_SAGITTA_RHO__1up", "MUON_SCALE__1down", "MUON_SCALE__1up", "MUON_TTVA_STAT__1down", "MUON_TTVA_STAT__1up", "MUON_TTVA_SYS__1down", "MUON_TTVA_SYS__1up"]
        elif mode == "JES":
            self.systematicsList = ["JET_EtaIntercalibration_NonClosure__1down", "JET_EtaIntercalibration_NonClosure__1up", "JET_BJES_Response__1up",   "JET_BJES_Response__1down",   "JET_EffectiveNP_Detector1__1up",   "JET_EffectiveNP_Detector1__1down",   "JET_EffectiveNP_Detector2__1up",   "JET_EffectiveNP_Detector2__1down",   "JET_EffectiveNP_Mixed1__1up",   "JET_EffectiveNP_Mixed1__1down",   "JET_EffectiveNP_Mixed2__1up",   "JET_EffectiveNP_Mixed2__1down",   "JET_EffectiveNP_Mixed3__1up",   "JET_EffectiveNP_Mixed3__1down",   "JET_EffectiveNP_Modelling1__1up",   "JET_EffectiveNP_Modelling1__1down",   "JET_EffectiveNP_Modelling2__1up",   "JET_EffectiveNP_Modelling2__1down",   "JET_EffectiveNP_Modelling3__1up",   "JET_EffectiveNP_Modelling3__1down",   "JET_EffectiveNP_Modelling4__1up",   "JET_EffectiveNP_Modelling4__1down",   "JET_EffectiveNP_Statistical1__1up",   "JET_EffectiveNP_Statistical1__1down",   "JET_EffectiveNP_Statistical2__1up",   "JET_EffectiveNP_Statistical2__1down",   "JET_EffectiveNP_Statistical3__1up",   "JET_EffectiveNP_Statistical3__1down",   "JET_EffectiveNP_Statistical4__1up",   "JET_EffectiveNP_Statistical4__1down",   "JET_EffectiveNP_Statistical5__1up",   "JET_EffectiveNP_Statistical5__1down",   "JET_EffectiveNP_Statistical6__1up",   "JET_EffectiveNP_Statistical6__1down",   "JET_EffectiveNP_Statistical7__1up",   "JET_EffectiveNP_Statistical7__1down",   "JET_EtaIntercalibration_Modelling__1up",   "JET_EtaIntercalibration_Modelling__1down", "JET_EtaIntercalibration_TotalStat__1up",   "JET_EtaIntercalibration_TotalStat__1down",   "JET_Flavor_Composition__1up",   "JET_Flavor_Composition__1down",   "JET_Flavor_Response__1up",   "JET_Flavor_Response__1down", "JET_Pileup_OffsetMu__1up",   "JET_Pileup_OffsetMu__1down",   "JET_Pileup_OffsetNPV__1up",   "JET_Pileup_OffsetNPV__1down",   "JET_Pileup_PtTerm__1up",   "JET_Pileup_PtTerm__1down",   "JET_Pileup_RhoTopology__1up",   "JET_Pileup_RhoTopology__1down",   "JET_PunchThrough_MC15__1up",   "JET_PunchThrough_MC15__1down",   "JET_SingleParticle_HighPt__1up",   "JET_SingleParticle_HighPt__1down", "JET_JvtEfficiency__1down", "JET_JvtEfficiency__1up"]
        elif mode == "JER":
            self.systematicsList = ["JET_JER_SINGLE_NP__1up"]
        elif mode == "Asym":
            self.systematicsList = ["JET_JER_SINGLE_NP__1up", "MET_SoftTrk_ResoPara", "MET_SoftTrk_ResoPerp"]
    def getsystematicsList(self):
        return self.systematicsList
