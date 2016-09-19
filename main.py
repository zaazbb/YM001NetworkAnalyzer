
import sys
from multiprocessing import Process, Pipe, freeze_support

from worker import worker


version = '0.0.1'


if __name__ == '__main__':
    freeze_support()
    
    conn_file = None
    if len(sys.argv) > 1:
        if sys.argv[1].upper().startswith('COM'):
            port = sys.argv[1]
            conn_file, child_conn = Pipe()
            p = Process(target=worker, args=(child_conn, sys.argv[1]), daemon=True)
            p.start()
        else:
            conn_file = sys.argv[1]
            
    import configparser
    from collections import OrderedDict
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    nodes = {'mnode': ['mnode', ''], 'node': OrderedDict(), 'xnode': {}}
    for i in config['DEFAULT']['nodes'].split(','):
        node = i.split()
        color = node[1] if len(node) > 1 else ''
        if node[0][0] == 'm':
            nodes['mnode'] = [node[0][1:13].zfill(12), color]
        elif node[0][0] == 'x':
            nodes['xnode'][node[0][1:13].zfill(12)] = color
        else:
            nodes['node'][node[0][:12].zfill(12)] = {'color': color, 'bpFlag': ''}
    #print(nodes)       
    
    from PyQt5.QtWidgets import QApplication
    from mainwindow import MainWindow
    
    app = QApplication(sys.argv)
    mainWin = MainWindow(conn_file, nodes, config)
    mainWin.show()
    
    sys.exit(app.exec_())
    
    p.join()
