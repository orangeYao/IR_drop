import json
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pylab as plt

dirs = './data/'

other_f = ['pos.json', 'slew.json', 'cap.json', 'twf.json']

seahawk_f = ['power.rpt']

resis = ['VDD_rlrp_inst.rpt', 'GND_rlrp_inst.rpt']

irs = ['GTBSM0SCTL_rail_analysis_tw_dynamic_ir_drop_cell.rpt',
       'GTBSM0SCTL_rail_analysis_tw_dynamic_ir_drop_clock.rpt']

def parse_json(dir, file):
    with open(dir + file) as f:
        data = json.load(f)
    return data


def parse_rpt_ir(dir, file):
    with open(dir + file) as f:
        data = f.readlines()
    rtn = {}
    for i in data:
        tmp = (i.split())
        rtn[tmp[0]] = tmp[2]
    return rtn


def parse_resis(dir, file, inf = 260):
    with open(dir + file, 'r') as f:
        x = f.read()
    x = x.replace('\n', '').replace('{\'name\': Instance(','').replace('\'value\':', '').replace('),', '')
    x = x.replace('\'', '').replace('}', '').split(',')
    x = [i.split() for i in x]

    names = set([i[0] for i in x])
    vals = {}
    for i in x:
        tmp = i[1].replace(']', '')
        if tmp == 'inf':
            tmp = inf 
        vals[i[0]] = float(tmp)
    return vals

def parse_rpt(dir, file):
    with open(dir + file) as f:
        data = f.readlines()[1:]
    rtn = {}
    for i in data:
        tmp = (i.split())
        rtn[tmp[0]] = [float(i) for i in tmp[2:]]
    return rtn

def parse_other():
    o_0 = parse_json(dirs, other_f[0])
    o_1 = parse_json(dirs, other_f[1])
    o_2 = parse_json(dirs, other_f[2])
    o_3 = parse_json(dirs, other_f[3])

    for i in o_0.keys():
        o_tmp = o_0[i]

        if i in o_1.keys():
            o_tmp['s'] = o_1[i]['s']
        else:
            o_tmp['s'] = 2.73e-11

        if i in o_2.keys():
            o_tmp['c'] = o_2[i]['c']
        else:
            o_tmp['c'] = 5.32e-15

        if i in o_3.keys():
            o_tmp['l'] = o_3[i]['l']
            o_tmp['u'] = o_3[i]['u']
        else:
            o_tmp['l'] = 0
            o_tmp['u'] = 0

    with open('cell_info_intermediate.json', 'w') as outfile:
        json.dump(o_0, outfile)


def parse_seahawk(d, f):
    j_dic = parse_json(d, f)
    seahawk = parse_rpt(dirs, seahawk_f[0])
    to_del_keys = []

    ris1 = parse_resis(dirs, resis[0], 260)
    ris2 = parse_resis(dirs, resis[1], 370)

    for i in j_dic.keys():
        j_tmp = j_dic[i]
        if i in seahawk:
            j_tmp['voltage'] = seahawk[i][0]
            j_tmp['tog'] = seahawk[i][1]
            j_tmp['all'] = seahawk[i][3]
            j_tmp['swit'] = seahawk[i][4]
            j_tmp['int'] = seahawk[i][5]
            j_tmp['leak'] = seahawk[i][6]
        else:
            print ('miss', i)
            to_del_keys.append(i)

        if i in ris1:
            j_tmp['ris'] = ris1[i] + ris2[i]
        else:
            print ('ris', i)

    print ('ignored num:', len(to_del_keys))
    for i in to_del_keys:
        del j_dic[i]

    print ('len,', len(j_dic))
    with open('seahawk.json', 'w') as outfile:
        json.dump(j_dic, outfile)


def parse_IR(d, f):
    j_dic = parse_json(d, f)
    to_del_keys = []
    r_dic_ir2 = {**parse_rpt_ir(dirs, irs[0]),
                 **parse_rpt_ir(dirs, irs[1])}

    for i in j_dic.keys():
        j_tmp = j_dic[i]

        if i in r_dic_ir2:
            j_tmp['ir'] = 0.94 - float(r_dic_ir2[i])
        else:
            print (i)
            to_del_keys.append(i)

    for i in to_del_keys:
        del j_dic[i]

    print ('len,', len(j_dic))
    with open('ir.json', 'w') as outfile:
        json.dump(j_dic, outfile)


if __name__ == '__main__':
    parse_other()
    parse_seahawk('./', 'cell_info_intermediate.json')
    parse_IR('./', 'cell_info_intermediate.json')

