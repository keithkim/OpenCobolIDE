import sys
from open_cobol_ide.compilers import GnuCobolCompiler
from pyqode.qt import QtCore, QtWidgets
from open_cobol_ide.view.forms import dlg_check_compiler_ui
from open_cobol_ide import system


class DlgCheckCompiler(QtWidgets.QDialog):
    def __init__(self, compiler, version, parent):
        super().__init__(
            parent, QtCore.Qt.WindowSystemMenuHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self._compiler = compiler
        self.ui = dlg_check_compiler_ui.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.plainTextEdit.setPlainText(version)
        self.ui.buttonBox.button(self.ui.buttonBox.Apply).setText(
            'Check compilation')
        self.ui.buttonBox.button(self.ui.buttonBox.Apply).clicked.connect(
            self._check_compiler)
        self.ui.buttonBox.button(self.ui.buttonBox.Apply).setDisabled(
            not version)

    def _check_compiler(self):
        output, exit_code = GnuCobolCompiler.check_compiler(self._compiler)

        if exit_code == 0:
            output = 'Compiler works!'
        else:
            output = 'Complier check failed:\n\nExit code: %d\nOutput:%s' % (
                exit_code, output)

        self.ui.label.setText('Output:')
        self.ui.plainTextEdit.setPlainText(output)

        if exit_code != 0:
            self.ui.plainTextEdit.appendPlainText(
                'Tips:\n- You might need to adapt the environment variables '
                'set by the IDE to make it work.')
            if system.windows:
                self.ui.plainTextEdit.appendPlainText(
                    '- If you see MinGW related errors ensure that there is no'
                    ' additional installation of MinGW in '
                    '%s:\MinGW' % sys.executable[0])

    @classmethod
    def check(cls, parent, compiler_path, version):
        dlg = cls(compiler_path, version, parent)
        return dlg.exec_() == dlg.Accepted
