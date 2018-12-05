
# PowerNet: predict IR drop with cell power using CNN.

## Overall
This repository contains python scripts for IR drop prediction with Convolutional Neural Network (CNN). The input feature is vectorless cell power and cell toggle rate given by Seahawk. We customized CNN architecture by a maximum structure.

## Raw Data
Take design 'GAASM0SMIO' as example.  
* Cell Information 
    * cap.json -- Cell capacitance
    * pos.json -- Cell coordinates
    * twf.json -- Cell rise/fall time
    * slew.json (not required) -- Cell slew 
* IR Information as label   
    * GAASM0SMIO_rail_analysis_tw_dynamic_ir_drop_cell.rpt -- Cell voltage (IR = 0.94 - voltage)
    * GAASM0SMIO_rail_analysis_tw_dynamic_ir_drop_clock.rpt -- Cell voltage (IR = 0.94 - voltage)
* Power Information
    * power.rpt -- Cell power from Seahawk
* Resistance Information(not required)
    * GND_rlrp_inst.rpt
    * VDD_rlrp_inst.rpt
* *Raw Data Location:
    - /home/scratch.sye_methodology_2/GAASM0SMIO_2p1p11_icc2_default/
        - ires/GAASM0SMIO.ipo201806290025.ires.10_15_16_29/intermediate_files/{cap, pos, twf, slew}.json
        - REPs/GAASM0SMIO_rail_analysis_tw_dynamic_ir_drop_{cell, clock}.rpt.gz
        - RUNs/GAASM0SMIO.ipo201806290025.rail_analysis/Reports/{power, GND_rlrp_inst, VDD_rlrp_inst}.rpt

## Required Library
- [Numpy](http://www.numpy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Pytorch (> 0.3.0)](https://pytorch.org/)
- [scikit-learn](https://scikit-learn.org/stable/)

## File Structure
- **design/**
Generate power features and IR drop label.
- **cnn/**
Train cnn model.
- **test_cnn/**
Generate inference results. Evaluate inference accuracy.


## Overall Flow
1. Build .json files with cell information (seahawk.json) and IR drop information (ir.json).  
```bash
    cd designs/design{1, 2, 3, 4}  
    python parse_all.py  
```
   Output: seahawk.json, ir.json

2. Generate power features & labels in 1um^2 grids  
```bash
    cd designs/design{1, 2, 3, 4}  
    python visual_designs.py (period, design size given in file)  
```
   Output: Time*.npy, ir.npy, Time_all*.png, ir.npy, ir.png  

3. Training  
```bash
    cd cnn  
    python cnn_{123, 124, 134, 234}.py  
```
   Output: cnn_{123, 124, 134, 234}*.pkl  


4. Inference  
```bash
    cd test_cnn  
    python test_all.py  
```
   Output: cnn_{123, 124, 134, 234}_{one, two, three, four}.npy  

5. Evaluate Inference  
```bash
    cd test_cnn  
    python plot.py  
    python roc.py  
    python eval.py  
```
Output: cnn_{123, 124, 134, 234}_{one, two, three, four}.png;  cnn_{123, 124, 134, 234}_{one, two, three, four}_roc.png

