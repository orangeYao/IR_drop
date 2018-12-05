

# PowerNet: predict IR drop with cell power using CNN.

## Overall
This repository contains python scripts for IR drop prediction with Convolutional Neural Network (CNN). The input feature is vectorless cell power and cell toggle rate given by Seahawk. We customized CNN architecture by a maximum structure.

## Raw Data
Take partition 'GAASM0SMIO' as example.  
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
* *Raw Data Location in Sheng Ye's scratch space:
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
* `design/` Generate power features and IR drop label.
    * `design{1,2,3,4}/` Four partitions available in this project. Each subfolder contains a different partition
    * `design1/data/` Contains raw data for corresponding partition
    * `design1/parse_all.py` Script generating .json file with cell information from raw data
    * `design1/visual_designs.py` Script generating power per time frame & IR drop
* `cnn/` Train cnn model.
    * `cnn_{123, 124, 134, 234}.py` Script taking different partitions for model training
* `test_cnn/` Generate inference results & evaluate inference accuracy.
    * `plot.py` Plot inference output and print TPR (recall) score
    * `roc.py` Plot ROC curve and print AUC of ROC for 1um^2 grid and 5um^2 grid
    * `eval.py` Print precision & recall for 1um^2 grid and 5um^2 grid
    

## Overall Flow
1. Build .json files with cell information and IR drop information  
```bash
    cd designs/design{1, 2, 3, 4}  
    python parse_all.py  
```
   Output: `seahawk.json` (.json with cell information), `ir.json` (.json with IR drop information)

2. Generate power features & labels in 1um^2 grids from .json files  
```bash
    cd designs/design{1, 2, 3, 4}  
    python visual_designs.py (period, design size given in file)  
```
   Output: `Time`**`i`**`.npy` (Grid power at time frame **i**), `ir.npy` (Grid IR drop), `Time_all*.png`, `ir.png`

3. Training  
```bash
    cd cnn  
    python cnn_{123, 124, 134, 234}.py  
```
   Output: `cnn_{123, 124, 134, 234}`**`j`**`.pkl` (CNN model trained with three partitions, epoch=(**j**+1)*20, i=0 is enough)

4. Perform Inference  
```bash
    cd test_cnn  
    python test_all.py  
```
   Output: `cnn_{123, 124, 134, 234}_{one, two, three, four}.npy`

5. Evaluate Inference Result
```bash
    cd test_cnn  
    python plot.py  
    python roc.py  
    python eval.py  
```
Output: `cnn_{123, 124, 134, 234}\_{one, two, three, four}.png`;  `cnn\_{123, 124, 134, 234}_{one, two, three, four}_roc.png`


