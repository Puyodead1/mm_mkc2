# Source Generated with Decompyle++
# File: forms.pyc (Python 2.5)

from PyQt4 import QtCore, QtGui
from movieDetailForm import DiscDetailForm
from moviePriceForm import DiscPriceForm
from movieAvailableNoticeForm import DiscAvailableNoticeForm
from shoppingCartForm import ShoppingCartForm
from couponForm import CouponForm
from checkoutSwipeCardForm import CheckOutSwipeCardForm
from checkOutEjectForm import CheckOutEjectForm
from checkOutResultForm import CheckOutResultForm
from checkoutChooseCardForm import CheckOutChooseCardForm
from checkoutSwipeDebitCardForm import CheckOutSwipeDebitCardForm
from checkOutSwipeChipPinForm import CheckOutSwipeChipPinForm
from checkOutSwipeSiTefForm import CheckOutSwipeSiTefForm
from checkOutSwipeProsaForm import CheckOutSwipeProsaForm
from returnTakeInForm import ReturnTakeInForm
from returnDiscListForm import ReturnDiscListForm
from returnSwipeCardForm import ReturnSwipeCardForm
from returnOptionForm import ReturnOptionForm
from returnResultForm import ReturnResultForm
from adminMainForm import AdminMainForm
from loadUpcEnterForm import LoadUpcEnterForm
from loadTitleForm import LoadTitleEnterForm
from loadDiscListForm import LoadDiscListForm
from loadDiscInfoForm import LoadDiscInfoForm
from loadTakeInForm import LoadTakeInForm
from loadResultForm import LoadResultForm
from unloadMarkedForm import UnloadMarkedForm
from unloadBySlotForm import UnloadBySlotForm
from unloadByTitleForm import UnloadByTitleForm
from unloadEjectForm import UnloadEjectForm
from unloadResultForm import UnloadResultForm
from configTestModeForm import ConfigTestModeForm
from configSpeakerVolumeForm import ConfigSpeakerVolumeForm
from configOperatorCodeForm import ConfigOperatorCodeForm
from configHDMIStateForm import ConfigHDMIStateForm
from configNetworkDiagnosisForm import ConfigNetworkDiagnosisForm
from configPowerOffForm import ConfigPowerOffForm
from superAdminMainForm import SuperAdminMainForm
from superAdminOffsetAdjForm import SuperAdminOffsetAdjForm
from superAdminDistanceForm import SuperAdminDistanceForm
from kioskInfoForm import KioskInfoForm
from reportForm import ReportForm
from pickupForm import PickUpSwipeCardForm
from pickupDiscListForm import PickUpDiscListForm
from pickupEjectForm import PickUpEjectForm
from pickupResultForm import PickUpResultForm
from pickupCodeForm import PickUpCodeForm
from recoverTakeInForm import RecoverTakeInForm
from initFailForm import InitFailForm
from fatalErrorForm import FatalErrorForm
from remoteArrangementForm import RemoteArrangementForm
from testMainForm import TestMainForm
from testingForm import TestingForm
from testTakeInForm import TestTakeInForm
from testResultForm import TestResultForm
from membershipCenterForm import MembershipCenterForm
from membershipLoginPasswordForm import MembershipLoginPasswordForm
from membershipLoginSwipeCardForm import MembershipLoginSwipeCardForm
from membershipCouponForm import MembershipCouponForm
from membershipProfileForm import MembershipProfileForm
from membershipTransactionForm import MembershipTransactionForm
from membershipLogoutForm import MembershipLogoutForm
from registerMainForm import RegisterMainForm
from registerResultForm import RegisterResultForm
from registerSwipeCardForm import RegisterSwipeCardForm
from cerepayCenterForm import CerepayCenterForm
from checkOutWithoutCerepayCardForm import CheckOutWithoutCerepayCardForm
from cerepayTopupMainForm import CerepayTopupMainForm
from cerepayTopupSwipeChinPinForm import CerepayTopupSwipeChinPinForm
from cerepayTopupSwipeCreditCardForm import CerepayTopupSwipeCreditCardForm
from cerepayTopupReceiptForm import CerepayTopupReceiptForm
from cerepayTopupErrorForm import CerepayTopupErrorForm
from returnManuallyTakeInForm import ReturnManuallyTakeInForm
from showAllSlotForm import ShowAllSlotForm
from config import pic_bg_rent
import sys

class Forms(QtGui.QWidget):
    
    def __init__(self, Game = 0):
        QtGui.QWidget.__init__(self)
        self.setGeometry(QtCore.QRect(0, 0, 768, 1024))
        self.setCursor(QtCore.Qt.BlankCursor)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.X11BypassWindowManagerHint)
        palette = QtGui.QPalette()
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(QtGui.QPixmap(pic_bg_rent)))
        self.setPalette(palette)
        self.FORMS = { }
        if not Game:
            MainForm = MainForm
            import mainForm
            RentMainForm = RentMainForm
            import rentForm
        else:
            MainForm = MainForm
            import mainForm_game
            RentMainForm = RentMainForm
            import rentForm_game
        self.FORMS['MainForm'] = MainForm()
        self.FORMS['RentMainForm'] = RentMainForm()
        self.FORMS['DiscDetailForm'] = DiscDetailForm()
        self.FORMS['DiscPriceForm'] = DiscPriceForm()
        self.FORMS['DiscAvailableNoticeForm'] = DiscAvailableNoticeForm()
        self.FORMS['ShoppingCartForm'] = ShoppingCartForm()
        self.FORMS['CouponForm'] = CouponForm()
        self.FORMS['CheckOutSwipeCardForm'] = CheckOutSwipeCardForm()
        self.FORMS['CheckOutEjectForm'] = CheckOutEjectForm()
        self.FORMS['CheckOutResultForm'] = CheckOutResultForm()
        self.FORMS['CheckOutChooseCardForm'] = CheckOutChooseCardForm()
        self.FORMS['CheckOutSwipeDebitCardForm'] = CheckOutSwipeDebitCardForm()
        self.FORMS['CheckOutSwipeChipPinForm'] = CheckOutSwipeChipPinForm()
        self.FORMS['CheckOutSwipeProsaForm'] = CheckOutSwipeProsaForm()
        self.FORMS['CheckOutSwipeSiTefForm'] = CheckOutSwipeSiTefForm()
        self.FORMS['ReturnTakeInForm'] = ReturnTakeInForm()
        self.FORMS['ReturnDiscListForm'] = ReturnDiscListForm()
        self.FORMS['ReturnSwipeCardForm'] = ReturnSwipeCardForm()
        self.FORMS['ReturnOptionForm'] = ReturnOptionForm()
        self.FORMS['ReturnResultForm'] = ReturnResultForm()
        self.FORMS['AdminMainForm'] = AdminMainForm()
        self.FORMS['LoadUpcEnterForm'] = LoadUpcEnterForm()
        self.FORMS['LoadTitleEnterForm'] = LoadTitleEnterForm()
        self.FORMS['LoadDiscListForm'] = LoadDiscListForm()
        self.FORMS['LoadDiscInfoForm'] = LoadDiscInfoForm()
        self.FORMS['UnloadMarkedForm'] = UnloadMarkedForm()
        self.FORMS['UnloadBySlotForm'] = UnloadBySlotForm()
        self.FORMS['UnloadByTitleForm'] = UnloadByTitleForm()
        self.FORMS['UnloadEjectForm'] = UnloadEjectForm()
        self.FORMS['UnloadResultForm'] = UnloadResultForm()
        self.FORMS['ConfigTestModeForm'] = ConfigTestModeForm()
        self.FORMS['ConfigSpeakerVolumeForm'] = ConfigSpeakerVolumeForm()
        self.FORMS['ConfigOperatorCodeForm'] = ConfigOperatorCodeForm()
        self.FORMS['ConfigHDMIStateForm'] = ConfigHDMIStateForm()
        self.FORMS['ConfigNetworkDiagnosisForm'] = ConfigNetworkDiagnosisForm()
        self.FORMS['ConfigPowerOffForm'] = ConfigPowerOffForm()
        self.FORMS['SuperAdminMainForm'] = SuperAdminMainForm()
        self.FORMS['SuperAdminOffsetAdjForm'] = SuperAdminOffsetAdjForm()
        self.FORMS['SuperAdminDistanceForm'] = SuperAdminDistanceForm()
        self.FORMS['KioskInfoForm'] = KioskInfoForm()
        self.FORMS['ReportForm'] = ReportForm()
        self.FORMS['PickUpSwipeCardForm'] = PickUpSwipeCardForm()
        self.FORMS['PickUpDiscListForm'] = PickUpDiscListForm()
        self.FORMS['PickUpEjectForm'] = PickUpEjectForm()
        self.FORMS['PickUpResultForm'] = PickUpResultForm()
        self.FORMS['PickUpCodeForm'] = PickUpCodeForm()
        self.FORMS['RecoverTakeInForm'] = RecoverTakeInForm()
        self.FORMS['InitFailForm'] = InitFailForm()
        self.FORMS['FatalErrorForm'] = FatalErrorForm()
        self.FORMS['RemoteArrangementForm'] = RemoteArrangementForm()
        self.FORMS['TestMainForm'] = TestMainForm()
        self.FORMS['TestingForm'] = TestingForm()
        self.FORMS['TestTakeInForm'] = TestTakeInForm()
        self.FORMS['TestResultForm'] = TestResultForm()
        self.FORMS['MembershipCenterForm'] = MembershipCenterForm()
        self.FORMS['MembershipLoginPasswordForm'] = MembershipLoginPasswordForm()
        self.FORMS['MembershipLoginSwipeCardForm'] = MembershipLoginSwipeCardForm()
        self.FORMS['MembershipCouponForm'] = MembershipCouponForm()
        self.FORMS['MembershipProfileForm'] = MembershipProfileForm()
        self.FORMS['MembershipTransactionForm'] = MembershipTransactionForm()
        self.FORMS['MembershipLogoutForm'] = MembershipLogoutForm()
        self.FORMS['ReturnManuallyTakeInForm'] = ReturnManuallyTakeInForm()
        self.FORMS['ShowAllSlotForm'] = ShowAllSlotForm()
        self.FORMS['RegisterMainForm'] = RegisterMainForm()
        self.FORMS['RegisterResultForm'] = RegisterResultForm()
        self.FORMS['RegisterSwipeCardForm'] = RegisterSwipeCardForm()
        self.FORMS['CerepayCenterForm'] = CerepayCenterForm()
        self.FORMS['CheckOutWithoutCerepayCardForm'] = CheckOutWithoutCerepayCardForm()
        self.FORMS['CerepayTopupMainForm'] = CerepayTopupMainForm()
        self.FORMS['CerepayTopupSwipeChinPinForm'] = CerepayTopupSwipeChinPinForm()
        self.FORMS['CerepayTopupSwipeCreditCardForm'] = CerepayTopupSwipeCreditCardForm()
        self.FORMS['CerepayTopupReceiptForm'] = CerepayTopupReceiptForm()
        self.FORMS['CerepayTopupErrorForm'] = CerepayTopupErrorForm()
        layout = QtGui.QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        for key in self.FORMS:
            layout.addWidget(self.FORMS[key], 0, 0)
            self.FORMS[key].hide()
        
        self.currentForm = 'MainForm'
        self.FORMS['LoadTakeInForm'] = LoadTakeInForm(self.FORMS['LoadDiscInfoForm'])
        self.FORMS['LoadResultForm'] = LoadResultForm(self.FORMS['LoadDiscInfoForm'])
        self.FORMS['LoadTakeInForm'].hide()
        self.FORMS['LoadResultForm'].hide()

    
    def getForm(self, wid):
        if wid in self.FORMS:
            return self.FORMS[wid]
        else:
            return -1

    
    def showForm(self, wid):
        form = self.getForm(wid)
        if form == -1:
            print('[showForm] Warning: no this form %s' % wid)
            return -1
        
        form.show()
        self.currentForm = wid

    
    def hideForm(self, wid):
        form = self.getForm(wid)
        if form == -1:
            print('[hideForm] Warning: no this form %s' % wid)
            return -1
        
        form.hide()

    
    def destroyForm(self, wid):
        form = self.getForm(wid)
        if form == -1:
            print('[destroyForm] Warning: no this form %s' % wid)
            return -1
        
        form.destroy()

    
    def getCurrentForm(self):
        return self.getForm(self.currentForm)

    
    def hideCurrentForm(self):
        self.getCurrentForm().hide()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Forms()
    form.show()
    form.showForm('CheckOutSwipeProsaForm')
    sys.exit(app.exec_())

