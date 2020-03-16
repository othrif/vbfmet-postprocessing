# Theory Uncertainties for V+jets #

To get started, copy the inputs from eos `/eos/atlas/atlascerngroupdisk/phys-exotics/jdm/vbfinv/theoryUnc/theoVariation_met200` to the `./input` directory and change the path in the code.

Run the following:
``` bash
python calculateOTFYields.py Z_strong SR # as an example
python runAllSystematics.py # runs all regions in one go
root interpolate.cxx # example on how to perform a linear fit
root plot_ckkw_resum.cxx # visualize the ckkw/resummation variations
```