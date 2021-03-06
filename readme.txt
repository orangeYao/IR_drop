
Raw Data:
    Cell Information:
        cap.json -- Cell capacitance
        pos.json -- Cell coordinates
        twf.json -- Cell rise/fall time
        slew.json (not required) -- Cell slew
    
    IR Information as label:
        GAASM0SMIO_rail_analysis_tw_dynamic_ir_drop_cell.rpt -- Cell voltage (IR = 0.94 - voltage)
        GAASM0SMIO_rail_analysis_tw_dynamic_ir_drop_clock.rpt -- Cell voltage (IR = 0.94 - voltage)

    Power Information:
        power.rpt -- Cell power from Seahawk

    Resistance Information(not required):
        GND_rlrp_inst.rpt
        VDD_rlrp_inst.rpt

    *Raw Data Location:
        /home/scratch.sye_methodology_2/GAASM0SMIO_2p1p11_icc2_default/
            ires/GAASM0SMIO.ipo201806290025.ires.10_15_16_29/intermediate_files/{cap, pos, twf, slew}.json
            REPs/GAASM0SMIO_rail_analysis_tw_dynamic_ir_drop_{cell, clock}.rpt.gz
            RUNs/GAASM0SMIO.ipo201806290025.rail_analysis/Reports/{power, GND_rlrp_inst, VDD_rlrp_inst}.rpt

Overall Flow:
    1. Build .json files with cell information (seahawk.json) and IR drop information (ir.json).
        cd designs/design{1, 2, 3, 4}
        python parse_all.py

       Output: seahawk.json, ir.json

    2. Generate power features & labels in 1um^2 grids
        cd designs/design{1, 2, 3, 4}
        python visual_designs.py (period, design size given in file)
        
       Output: Time*.npy, ir.npy, Time_all*.png, ir.npy, ir.png

    3. Training
        cd cnn
        python cnn_{123, 124, 134, 234}.py

       Output: cnn_{123, 124, 134, 234}*.pkl

    4. Inference
        cd test_cnn
        python test_all.py

       Output: cnn_{123, 124, 134, 234}_{one, two, three, four}.npy

    5. Evaluate Inference
        cd test_cnn
        python plot.py
        python roc.py
        python eval.py

Required:
    Numpy
    Matplotlib
    Pytorch (> 0.3.0)


