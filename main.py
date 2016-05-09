
import sys
from multiprocessing import Process, Pipe

from worker import worker


if __name__ == '__main__':
    conn_file = None
    if len(sys.argv) > 1:
        if sys.argv[1].upper().startswith('COM'):
            conn_file, child_conn = Pipe()
            p = Process(target=worker, args=(child_conn, sys.argv[1]), daemon=True)
            p.start()
        else:
            conn_file = sys.argv[1]
    
    from PyQt5.QtWidgets import QApplication
    from mainwindow import MainWindow
    
    app = QApplication(sys.argv)
    mainWin = MainWindow(conn_file)
    mainWin.show()
    
    sys.exit(app.exec_())
    
    p.join()
