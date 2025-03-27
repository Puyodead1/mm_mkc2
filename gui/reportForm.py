# Source Generated with Decompyle++
# File: reportForm.pyc (Python 2.5)

'''
ReportForm 
2009-07-29 created by Mavis
'''
import os
import sys
from PyQt4 import QtCore, QtGui
from reportForm_ui import Ui_reportForm
import config
import component

class ReportForm(QtGui.QWidget):
    
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_reportForm()
        self.ui.setupUi(self)
        self.setGeometry(0, 0, 768, 1024)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(config.pic_bg_report)))
        self.setPalette(palette)
        self.ui.btn_logout = component.btnLogout(self, 'ReportForm')
        self.ui.btn_logout.setGeometry(580, 20, 160, 68)
        self.ui.btn_cancel = component.btnCancel(self, 'ReportForm')
        self.ui.btn_back = component.btnBack(self, 'ReportForm')
        self.ui.hboxlayout1.addWidget(self.ui.btn_cancel)
        self.ui.hboxlayout1.addWidget(self.ui.btn_back)
        self.ui.gridLayout.setGeometry(QtCore.QRect(65, 195, 660, 165))
        self.ui.gridLayout.setStyleSheet('font: bold 18px')
        self.ui.gridLayout_2.setGeometry(QtCore.QRect(65, 410, 390, 160))
        self.ui.gridLayout_2.setStyleSheet('font: bold 17px')
        self.ui.gridLayout_3.setGeometry(QtCore.QRect(45, 610, 670, 5 * 37 + 40))
        self.ui.gridLayout_3.setStyleSheet('font: bold 17px')
        style = 'font: bold 18px'
        self.ui.today.setStyleSheet('font: bold 22px; text-align: top')
        self.ui.label_today.setStyleSheet('font: bold 22px; text-align: top')
        self.ui.label_y.setStyleSheet(style)
        self.ui.label_m.setStyleSheet(style)
        self.ui.label_w.setStyleSheet(style)
        self.ui.ctr_report = component.virtualComponent(self)

    
    def setReport(self, data):
        if not data:
            return -1
        
        data = data['ctr_report']
        for key in data:
            if eval('getattr(self.ui, "' + key + '", None)') != None:
                exec('self.ui.' + key + '.setText("' + data[key] + '")')
            
        

    
    def showEvent(self, event):
        self.ui.retranslateUi('')
        self.ui.btn_logout.reset()
        self.ui.btn_cancel.hide()
        self.ui.btn_back.reset()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mainf = ReportForm()
    mainf.show()
    data = {
        'ctr_report': {
            'initial_rentals_week': '3',
            'rental_income_month': '0.00',
            'sale_income_month': '0.00',
            'sale_income': '0.00',
            'total_empty_slots': '246',
            'total_dvds_in': '7',
            'completed_rentals_week': '0',
            'total_dvds_out': '0',
            'capacity': '253',
            'initial_rentals_year': '3',
            'rental_income_week': '0.00',
            'initial_rentals': '3',
            'sale_income_year': '0.00',
            'total_loaded_dvd': '7',
            'rental_income_year': '0.00',
            'sale_count_year': '0',
            'initial_rentals_month': '3',
            'today': '2009-07-31',
            'rental_income': '0.00',
            'total_tax': '0.00',
            'kiosk_id': 'S250-A912',
            'total_dvds_reserved': '0',
            'completed_rentals': '0',
            'sale_count_week': '0',
            'sale_income_week': '0.00',
            'sale_count': '0',
            'total_income': '0.00',
            'completed_rentals_year': '0',
            'sale_count_month': '0',
            'completed_rentals_month': '0' } }
    mainf.ui.ctr_report.setReport(data)
    sys.exit(app.exec_())

