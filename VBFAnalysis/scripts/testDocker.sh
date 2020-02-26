

TESTFILE_ORIGINS=("root://eosatlas.cern.ch//eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/RECAST/input/MiniNtuple_Signal/user.othrif.vXX.999999.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_ZZ4nu_MET75.root/user.othrif.vXX.999999.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_ZZ4nu_MET75.root")
TEST_DIRS=("input_files/user.othrif.vXX.999999.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_ZZ4nu_MET75.root")
i_type=0

while [  $i_type -lt 1 ]; do

  echo "RUNNING TEST OF NTUPLING : " "${TESTFILE_ORIGINS[$i_type]}"

  ##############################
  # Process test sample        #
  ##############################

  # create directory for results
  pwd
  mkdir -p "${TEST_DIRS[$i_type]}"
  #cd "${TEST_DIRS[$i_type]}"
  #pwd

  # copy file with xrdcp
  if [ ! -f "${TESTFILE_LOCALS[$i_type]}" ]; then
      echo "File not found! Copying it from EOS"
      # get kerberos token with service account  to access central test samples on EOS
      echo "Setting up kerberos"
      echo "CERN_USER - "${KRB_USERNAME}
      echo "SERVICE_PASS - "${KRB_PASSWORD}
      echo ${KRB_PASSWORD} | kinit ${KRB_USERNAME} #@CERN.CH

      echo xrdcp "${TESTFILE_ORIGINS[$i_type]}" "${TEST_DIRS[$i_type]}"
      xrdcp "${TESTFILE_ORIGINS[$i_type]}" "${TEST_DIRS[$i_type]}"
  fi

echo "$PWD/${TEST_DIRS[$i_type]}" > list
cat list
python /analysis/src/VBFAnalysis/util/getN.py -l list -o fout.root
athena VBFAnalysis/VBFAnalysisAlgJobOptions.py --filesInput ${TEST_DIRS[$i_type]}/user.othrif.vXX.999999.PowhegPy8EG_NNPDF30_AZNLOCTEQ6L1_VBFH125_ZZ4nu_MET75.root - --currentVariation Nominal - --normFile fout.root
mkdir -p output_files
hadd output_files/VBFH125.root  VBFH125*.root

athena VBFAnalysis/HFInputJobOptions.py --filesInput ../output_files/VBFH125.root - --currentVariation Nominal --Binning 11 --extraVars 7
mkdir -p HF_files
hadd HF_files/HFVBFHAltSignalNominal.root HFVBFHAltSignalNominal*root



done

echo "DONE"