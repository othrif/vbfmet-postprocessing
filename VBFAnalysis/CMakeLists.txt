# Declare the package
atlas_subdir( VBFAnalysis )

# Declare the package's dependencies:
atlas_depends_on_subdirs( PUBLIC
                          Control/AthToolSupport/AsgTools
                          Control/xAODRootAccess
                          Event/xAOD/xAODEventInfo
                          Event/xAOD/xAODJet
			  Event/xAOD/xAODCore
                          Event/xAOD/xAODMissingET
			  Reconstruction/Jet/BoostedJetTaggers
#                          xAODAnaHelpers
                          PRIVATE
                          Event/xAOD/xAODEgamma
                          Event/xAOD/xAODMuon
			  PhysicsAnalysis/AnalysisCommon/PATInterfaces
                          Tools/PathResolver )

# Declare external dependencies ... default here is to include ROOT
find_package( ROOT COMPONENTS MathCore RIO Core Tree Hist )

# Declare package as a library
# Note the convention that library names get "Lib" suffix
# Any package you depend on you should add
# to LINK_LIBRARIES line below (see the example)
atlas_add_library( VBFAnalysisLib src/*.cxx
                   PUBLIC_HEADERS VBFAnalysis
                   INCLUDE_DIRS ${ROOT_INCLUDE_DIRS}
                   LINK_LIBRARIES ${ROOT_LIBRARIES}
                                    AthAnalysisBaseCompsLib
				      AsgTools
  xAODEgamma
  xAODEventInfo
  xAODJet
  xAODCore
  xAODMissingET
  xAODMuon
  BoostedJetTaggersLib
  xAODRootAccess
  PathResolver
  PATInterfaces
  SUSYToolsLib
)

# if you add athena components (tools, algorithms) to this package
# these lines are needed so you can configure them in joboptions
atlas_add_component( VBFAnalysis src/components/*.cxx
                      NOCLIDDB
                      LINK_LIBRARIES VBFAnalysisLib
)

# if you add an application (exe) to this package
# declare it like this (note convention that apps go in the util dir)
# atlas_add_executable( MyApp util/myApp.cxx
#                       LINK_LIBRARIES VBFAnalysisLib
# )

# Install python modules, joboptions, and share content
atlas_install_python_modules( python/*.py )
atlas_install_python_modules( python/*/*.py )
atlas_install_scripts( scripts/*.py )
atlas_install_scripts( scripts/*.sh )
atlas_install_joboptions( share/*.py )
atlas_install_data( data/* )
# You can access your data from code using path resolver, e.g.
# PathResolverFindCalibFile("VBFAnalysis/file.txt")
#PathResolverFindCalibFile("VBFAnalysis/data/PMGxsecDB_mc16.txt")

