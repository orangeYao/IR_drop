from visual_designs_helper import *
import numpy as np

box_urx = 1038 
box_ury = 820
period = 7.1e-10
gcell = 1.0

cell_list = parse_json('./', 'seahawk.json')
for i in range(1, 51):
    print ('Time_all_' + str(i))
    print (i*period/50)
    b = construct_board_t(cell_list, 'Time_' + str(i), 'all', box_urx, box_ury, gcell, 25, i*period/50)
    np.save('Time_' + str(i), b)

cell_list = parse_json('./', 'ir.json')
b = construct_board_ave (cell_list, 'ir', 'ir', box_urx, box_ury, gcell, scale=0.2)
np.save('ir', b)

