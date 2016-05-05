
from multiprocessing import Process, Pipe

from worker import worker


if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=worker, args=(child_conn,), daemon=True)
    p.start()
    
    import sys
    from PyQt5.QtWidgets import QApplication
    from mainwindow import MainWindow

    app = QApplication(sys.argv)
    mainWin = MainWindow(parent_conn)
    mainWin.show()
    
    sys.exit(app.exec_())
    
    #p.join()
