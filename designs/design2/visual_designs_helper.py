import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import json
import math
import numpy as np


def add_shape(board, llx, lly, urx, ury, value):
    board[llx:urx, lly:ury] += value

def process_all(board, visl_list, gcell, process_type, t):
    if process_type == 'cell_loc':
        for i in visl_list:
            add_shape(board, int(math.floor(i['x1']/gcell)), int(math.floor(i['y1']/gcell)),
                             int(math.ceil(i['x2']/gcell)), int(math.ceil(i['y2']/gcell)), 1)
    elif process_type in ['all', 'swit', 'int', 'leak']:
        for i in visl_list:
            a =   (int(math.ceil(i['x2']/gcell)) - int(math.floor(i['x1']/gcell))
                )*(int(math.ceil(i['y2']/gcell)) - int(math.floor(i['y1']/gcell)))

            tt = int((i['l']<t) and (i['u']>t))
            add_shape(board, int(math.floor(i['x1']/gcell)), int(math.floor(i['y1']/gcell)),
                             int(math.ceil(i['x2']/gcell)), int(math.ceil(i['y2']/gcell)), i[process_type]*1e6 *tt/a)
    elif process_type in ['all_no_s', 'swit_no_s', 'int_no_s']:
        process_type = process_type[0:-5]
        for i in visl_list:
            a =   (int(math.ceil(i['x2']/gcell)) - int(math.floor(i['x1']/gcell))
                )*(int(math.ceil(i['y2']/gcell)) - int(math.floor(i['y1']/gcell)))

            tt = int((i['l']<t) and (i['u']>t))
            if i['tog'] != 0:
                tmp = i[process_type]/i['tog']*1e6
            else:
                tmp = i[process_type]*1e6
            add_shape(board, int(math.floor(i['x1']/gcell)), int(math.floor(i['y1']/gcell)),
                             int(math.ceil(i['x2']/gcell)), int(math.ceil(i['y2']/gcell)), tmp *tt/a)
    elif process_type not in visl_list[0]:
        print('Type does not exist!!', process_type)
        exit()
    else:
        for i in visl_list:
            add_shape(board, int(math.floor(i['x1']/gcell)), int(math.floor(i['y1']/gcell)),
                             int(math.ceil(i['x2']/gcell)), int(math.ceil(i['y2']/gcell)), i[process_type])

def construct_board_t(visl_list, name, process_type, box_urx, box_ury, gcell, scale, t):
    box_width = int(math.ceil(box_urx/gcell))
    box_height = int(math.ceil(box_ury/gcell))
    board = np.zeros((box_width, box_height))
    process_all(board, visl_list, gcell, process_type, t)
    plot(board, name, scale)
    return board


def construct_board_ave(visl_list, name, process_type, box_urx, box_ury, gcell, scale=0.2):
    box_width = int(math.ceil(box_urx/gcell))
    box_height = int(math.ceil(box_ury/gcell))
    board = np.zeros((box_width, box_height))
    process_all(board, visl_list, gcell, process_type, None)

    board2 = np.zeros((box_width, box_height))
    process_all(board2, visl_list, gcell, 'cell_loc', None)
    board2 = np.clip (board2, 1, None)
    rtn = board / board2
    plot(rtn, name, scale)
    return rtn


def plot(board, name='tests', scale=0.2):
    fig = plt.figure(figsize=(10,10))
    ax = plt.gca()
    ax.set_aspect('equal')
    masked_array = np.ma.array (board, mask=board < 0.001*board.mean())
    cmap = matplotlib.cm.jet
    cmap.set_bad('white',1.)

    plt.imshow(np.flipud(np.rot90(masked_array)), origin='lower', vmax = scale,
                cmap = cmap)
    plt.colorbar(orientation='vertical')
    plt.title(name, fontsize=22)
    plt.close()
    fig.savefig(name, dpi=500)


def parse_json(dir, file):
    with open(dir + file) as f:
        data_cp = json.load(f)
    return list(data_cp.values())

