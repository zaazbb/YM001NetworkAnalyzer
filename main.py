
import sys
import configparser
#from multiprocessing import Process, Pipe, freeze_support
from multiprocessing import Pipe, freeze_support
from multiprocessing.context import Process


from worker import worker


version = '0.0.3'


if __name__ == '__main__':
    freeze_support()

    config = configparser.ConfigParser()
    config.read('config.ini')
    chnlgrp = config['DEFAULT'].getint('channelgroup')
    s=config['DEFAULT']['sendchannel']

    conn_file = None
    if len(sys.argv) > 1:
        if sys.argv[1] == 'listports':
            from serial.tools.list_ports import comports
            for i in comports():
                    print(list(i)[0])
            sys.exit(0)
        
        if sys.argv[1].upper().startswith('COM'):
            conn_file, child_conn = Pipe()
            p = Process(target=worker,
                        args=(child_conn, sys.argv[1],
                              config['DEFAULT'].getint('bypass_type'),
                              chnlgrp),
                        daemon=True)
            p.start()
        else:
            conn_file = sys.argv[1]

    from collections import OrderedDict
    
    nodes = {'mnode': ['mnode', ''], 'node': OrderedDict(), 'xnode': {}}
    for i in config['DEFAULT']['nodes'].split(','):
        node = i.split()
        color = node[1] if len(node) > 1 else ''
        addr = node[0].lstrip('mx0')
        if not addr:
            addr = '0'
        if node[0][0] == 'm':
            nodes['mnode'] = [addr, color]
        elif node[0][0] == 'x':
            nodes['xnode'][addr] = color
        else:
            nodes['node'][addr] = {'color': color}
    #print(nodes)       
    
    from PyQt5.QtWidgets import QApplication
    from mainwindow import MainWindow
    
    app = QApplication(sys.argv)
    mainWin = MainWindow(conn_file, nodes, chnlgrp, config)
    mainWin.setWindowTitle('NetworkAnalyzer_v' + version)
    mainWin.show()
    
    sys.exit(app.exec_())
    
    p.join()
