# CadenceToolViewerWidget.py
# (C)2013
# Scott Ernst

import os
import markdown

from PySide import QtGui

from pyaid.ClassUtils import ClassUtils

from pyglass.gui.scrollArea.SimpleScrollArea import SimpleScrollArea
from pyglass.web.PyGlassWebView import PyGlassWebView
from pyglass.widgets.PyGlassWidget import PyGlassWidget
from pyglass.widgets.LineSeparatorWidget import LineSeparatorWidget

from cadence.views.tools.ToolViewerHeaderElement import ToolViewerHeaderElement
from cadence.views.tools.ToolsHelpCommunicator import ToolsHelpCommunicator

#___________________________________________________________________________________________________ CadenceToolViewerWidget
class CadenceToolViewerWidget(PyGlassWidget):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

    _HTML_WRAPPER = """\
        <!doctype html>
        <head></head>
        <body style="font-size:70%;color:#333;">##CONTENT##</body>
        </html>
    """

#___________________________________________________________________________________________________ __init__
    def __init__(self, parent, **kwargs):
        """Creates a new instance of CadenceToolViewerWidget."""
        super(CadenceToolViewerWidget, self).__init__(parent, widgetFile=False, **kwargs)

        self._definition = None

        mainLayout = self._getLayout(self, QtGui.QVBoxLayout)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        self._header = ToolViewerHeaderElement(self)
        mainLayout.addWidget(self._header)

        focalBox, focalLayout = self._createElementWidget(self, QtGui.QHBoxLayout, True)

        self._toolScroller = SimpleScrollArea(focalBox)
        focalLayout.addWidget(self._toolScroller)
        self._toolBox = self._toolScroller.containerWidget
        self._getLayout(self._toolBox, QtGui.QVBoxLayout)
        self._containerWidget = self._toolBox

        w, l = self._createWidget(focalBox, QtGui.QHBoxLayout, True)
        self._helpBox = w

        sep = LineSeparatorWidget(w, False)
        l.addWidget(sep)

        self._helpComm    = ToolsHelpCommunicator()
        web = PyGlassWebView(w, communicator=self._helpComm, debug=True)
        web.openUrl('http://web.localhost.com/help/toolHelpContainer.html')
        web.setFixedWidth(360)
        self._helpWebView = web
        l.addWidget(self._helpWebView)

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _activateWidgetDisplayImpl
    def _activateWidgetDisplayImpl(self, **kwargs):
        d = kwargs.get('definition', None)
        self._definition = d

        self._header.setLabel(d['name'])
        if d['id'] not in self._widgetClasses:
            widgetClass = ClassUtils.dynamicImport(d['module'])
            self.addWidgetChild(d['id'], widgetClass, True)
        self.setActiveWidget(d['id'])

        self._helpBox.setVisible(self._helpComm.loadContent(self._currentWidget))

