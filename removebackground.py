import config
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from PyQt5.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QTextEdit, QProgressBar,
                             QFileDialog, QListView, QAbstractItemView, QComboBox,
                             QDialog, QGridLayout, QHBoxLayout, QHeaderView, QLabel,
                             QProgressDialog, QPushButton, QSizePolicy, QTableWidget,
                             QTableWidgetItem, QSlider, QSpinBox, QToolButton, QStyle,
                             QCheckBox, QGroupBox, QBoxLayout, QMessageBox, QAction,
                             QFileDialog, QMainWindow, QMessageBox, QTextEdit, QMenu, QFrame, QRadioButton)
from PyQt5 import QtCore  # conda install pyqt
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from  matplotlib.figure import Figure
import config
import numpy as np
import cv2
import matplotlib.pyplot as plt
import sys
import random
import math

from config import backgroundpanel
import imagedisplay as ImD


class RemovebackgroundWindow(QtWidgets.QWidget):

    def __init__(self,parent=None):

        super(RemovebackgroundWindow, self).__init__(parent)
        
        #.left = 300
        #self.top = 300
        #self.width = 300
        #self.height = 400

       # if config.DispState  == 0:
       #     return 
        
        
        self.setGeometry(backgroundpanel.left, backgroundpanel.top, backgroundpanel.width, backgroundpanel.height)

        self.setWindowTitle("Remove Background")

        self.main_layout = QVBoxLayout()

        # Plane group box
        self.plane_group_box = QGroupBox("Plane")
        self.plane_group_box.setFixedSize(200, 50)
        self.plane_layout = QHBoxLayout()
        
        self.rb_auto_checkbox = QCheckBox("Auto")
        self.rb_auto_checkbox.setChecked(config.rb_plane_auto)  # all_Filterに依存して初期値を設定
        self.rb_auto_checkbox.stateChanged.connect(self.on_auto_checkbox_changed)
        self.plane_layout.addWidget(self.rb_auto_checkbox)
        #self.plane_layout.setSpacing(1)

        self.plane_order_label = QLabel("Order")
        self.plane_order_spin_box = QSpinBox()
        self.plane_order_spin_box.setRange(1, 5)
        self.plane_order_spin_box.setValue(config.rb_plane_order)  # rb_plane_orderに応じて初期値を設定
        self.plane_order_spin_box.valueChanged.connect(self.update_plane_order)

        self.plane_order_layout = QHBoxLayout()
        self.plane_order_layout.setSpacing(1)  # ここで order_label と order_spin_box の間のスペースを調整  
        self.plane_order_layout.addWidget(self.plane_order_label)
        self.plane_order_layout.addWidget(self.plane_order_spin_box)        

        self.plane_layout.addLayout(self.plane_order_layout)
        self.plane_group_box.setLayout(self.plane_layout)

        # Line-by-Line group box
        self.line_by_line_group_box = QGroupBox("Line-by-Line")
        self.line_by_line_group_box.setFixedSize(200, 150)
        self.line_by_line_layout = QVBoxLayout()

        # Add combo box for selecting direction
        self.direction_combo_box = QComboBox()
        self.direction_combo_box.addItem("Horizontal")
        self.direction_combo_box.addItem("Vertical")
        self.direction_combo_box.setCurrentText(config.rb_line_direction)  # rb_line_directionに応じて初期値を設定
        self.direction_combo_box.currentIndexChanged.connect(self.update_direction)
        self.line_by_line_layout.addWidget(self.direction_combo_box)
        
        self.off_radio_button = QRadioButton("Off")
        self.off_radio_button.toggled.connect(self.update_rb_line_type)
        self.line_by_line_layout.addWidget(self.off_radio_button)

        self.polynomial_order_layout = QHBoxLayout()
        #self.polynomial_order_layout.setSpacing(10)  # ここでスペーシングを調整
        self.polynomial_radio_button = QRadioButton("Polynomial")
        self.polynomial_radio_button.toggled.connect(self.update_rb_line_type)

        
        self.polynomial_order_layout.addWidget(self.polynomial_radio_button)

        self.polynomial_order_layout.addSpacing(1)  # ここにスペースを追加

        self.line_order_label= QLabel("Order")
        self.line_order_spin_box = QSpinBox()
        self.line_order_spin_box.setSingleStep(1)
        self.line_order_spin_box.setRange(1, 5)
        self.line_order_spin_box.setValue(config.rb_line_order)  # rb_line_orderに応じて初期値を設定
        self.line_order_spin_box.valueChanged.connect(self.update_line_order)
       

        self.line_order_layout = QHBoxLayout()
        self.line_order_layout.setSpacing(2)  # ここでスペーシングを調整
        self.line_order_layout.addWidget(self.line_order_label)
        self.line_order_layout.addWidget(self.line_order_spin_box)

        self.polynomial_order_layout.addLayout(self.line_order_layout)
        self.line_by_line_layout.addLayout(self.polynomial_order_layout)

        self.median_radio_button = QRadioButton("Median")
        self.median_radio_button.toggled.connect(self.update_rb_line_type)

        self.mediandiff_radio_button = QRadioButton("Median Difference")
        self.mediandiff_radio_button.toggled.connect(self.update_rb_line_type)

        self.histogram_radio_button = QRadioButton("Histogram")
        self.histogram_radio_button.toggled.connect(self.update_rb_line_type)

       # Create a slider widget
        self.histogram_slider = QSlider(Qt.Horizontal)
        self.histogram_slider.setMinimum(0)
        self.histogram_slider.setMaximum(100)
        self.histogram_slider.setValue(config.rb_histogram_slider_value)  # Set initial value
        self.histogram_slider.setTickInterval(10)
        self.histogram_slider.setTickPosition(QSlider.TicksBelow)
        self.histogram_slider.valueChanged.connect(self.update_histogram_slider_value)
        # Add the slider to the layout, but hide it initially
        self.line_by_line_layout.addWidget(self.histogram_slider)
        self.histogram_slider.hide()

        # Show the slider when the "Histogram" radio button is selected
        self.histogram_radio_button.toggled.connect(self.histogram_slider.setVisible)

        
        if config.rb_line_type == 0:
            self.off_radio_button.setChecked(True)
        elif config.rb_line_type == 1:
            self.polynomial_radio_button.setChecked(True)
        elif config.rb_line_type == 2:
            self.median_radio_button.setChecked(True)
        elif config.rb_line_type == 3:
            self.mediandiff_radio_button.setChecked(True)
        elif config.rb_line_type == 4:
            self.histogram_radio_button.setChecked(True)
        
        
        self.line_by_line_layout.addWidget(self.median_radio_button)
        self.line_by_line_layout.addWidget(self.mediandiff_radio_button)
        self.line_by_line_layout.addWidget(self.histogram_radio_button)
        

        self.line_by_line_group_box.setLayout(self.line_by_line_layout)

        self.main_layout.addWidget(self.plane_group_box)
        self.main_layout.addWidget(self.line_by_line_group_box)

        self.setLayout(self.main_layout)

    def update_histogram_slider_value(self, value):
        # Update config value when slider value is changed
        config.rb_histogram_slider_value = value

    def update_rb_line_type(self):
        if self.off_radio_button.isChecked():
            config.rb_line_type = 0
        elif self.polynomial_radio_button.isChecked():
            config.rb_line_type = 1
        elif self.median_radio_button.isChecked():
            config.rb_line_type = 2
        elif self.mediandiff_radio_button.isChecked():
            config.rb_line_type = 3
        elif self.histogram_radio_button.isChecked():
            config.rb_line_type = 4

        self.update_image()

    def update_direction(self, index):
        if index == 0:
            config.rb_line_direction= "Horizontal"
        elif index == 1:
            config.rb_line_direction = "Vertical"
        # Update other functions or variables based on the selected direction

        self.update_image()

    def update_plane_order(self):

        config.rb_plane_order = self.plane_order_spin_box.value()

        self.update_image()
    
    def update_line_order(self):

        config.rb_line_order = self.line_order_spin_box.value()

        self.update_image()

    def on_auto_checkbox_changed(self, state):    
        
        if state == Qt.Checked:
            
            config.rb_plane_auto= 1
  
        else:
            
            config.rb_plane_auto = 0
            

        self.update_image()       

    def update_image(self):

        if config.rb_plane_auto == 1:

            #config.ZaryData = cv2.blur(config.RawaryData, ksize=(config.kernel_size , config.kernel_size ))  

            # 最小二乗フィッティングの準備
            rows, cols = config.RawaryData.shape
            x, y = np.meshgrid(np.arange(cols), np.arange(rows))

            # 特徴行列Xを作成
            X = np.column_stack([x.ravel()**i * y.ravel()**j for i in range(config.rb_plane_order+1) for j in range(config.rb_plane_order+1) if i+j <= config.rb_plane_order])
            Y = config.RawaryData.ravel()

            # 最小二乗フィッティング
            coeffs, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)

            # 同じ次元の二次元配列にフィッティング結果を適用
            config.ZaryData = config.RawaryData- (X @ coeffs).reshape(rows, cols)
        

        
        if config.rb_line_type == 0 and config.rb_plane_auto == 0:
            
            config.ZaryData = np.array(config.RawaryData)
        
        
        fitdata = np.zeros_like(config.RawaryData)  # 全ての要素が0の配列を作成する（arraydataと同じ形状）
        tempdata = np.zeros_like(config.RawaryData)

        if config.rb_line_type !=0 :
                
            if config.rb_line_direction == "Horizontal":
                    
                tempdata = np.array(config.RawaryData)
                
            elif config.rb_line_direction == "Vertical":
                    
                tempdata = np.array(config.RawaryData.T)

            if config.rb_line_type == 1: # Polynomianl fitting

                # 各行に対して最小二乗フィッティングを行い、結果を格納する新しい配列を作成する
                     
                fitdata = np.zeros_like(tempdata)  # 全ての要素が0の配列を作成する（arraydataと同じ形状）

                for i, row in enumerate(tempdata):
                    x = np.arange(len(row))
                    y = row
                    coeffs = np.polyfit(x, y, config.rb_line_order)  # order次の最小二乗フィッティングを行う
                    fitdata[i] =np.polyval(coeffs, x)  # フィッティング曲線のy値を計算し、fitdataに格納する
        
            elif config.rb_line_type == 2 or config.rb_line_type == 3 : # median or median diffence
            
                #二次元配列arraydataの各行ごとに、各列のデータの中央値を二次元配列にして戻す関数。

                fitdata = np.zeros((tempdata.shape[0], tempdata.shape[1]))
                median_all = np.median(tempdata)

                for i, row in enumerate(tempdata):
                    median = np.median(row)  # 各行の中央値を計算する

                    if config.rb_line_type == 2:
                        fitdata[i] = np.full(tempdata.shape[1], median)  # 中央値を各列に入れる
                    elif config.rb_line_type == 3:
                        fitdata[i] = np.full(tempdata.shape[1], median)-median_all

            elif config.rb_line_type == 4 : # Histogram
               
              self.histogram_slider.show()
            
            tempdata -= fitdata

            if config.rb_line_direction == "Horizontal":
                    
                config.ZaryData =tempdata
            
            elif config.rb_line_direction == "Vertical":

                config.ZaryData =tempdata.T
  


        disp = ImD.ImageDisplay()
        disp.DispAryData()

    
def Removebackrgoud_Plane():

    #config.ZaryData = cv2.blur(config.RawaryData, ksize=(config.kernel_size , config.kernel_size ))  

    # 最小二乗フィッティングの準備
    rows, cols = config.RawaryData.shape
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))

    # 特徴行列Xを作成
    X = np.column_stack([x.ravel()**i * y.ravel()**j for i in range(config.rb_plane_order+1) for j in range(config.rb_plane_order+1) if i+j <= config.rb_plane_order])
    Y = config.RawaryData.ravel()

    # 最小二乗フィッティング
    coeffs, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)


    # 同じ次元の二次元配列にフィッティング結果を適用
    config.ZaryData = config.RawaryData- (X @ coeffs).reshape(rows, cols)

def Removebackrgoud_Line():

    if config.rb_plane_auto == 1:

        #config.ZaryData = cv2.blur(config.RawaryData, ksize=(config.kernel_size , config.kernel_size ))  

        # 最小二乗フィッティングの準備
        rows, cols = config.RawaryData.shape
        x, y = np.meshgrid(np.arange(cols), np.arange(rows))

        # 特徴行列Xを作成
        X = np.column_stack([x.ravel()**i * y.ravel()**j for i in range(config.rb_plane_order+1) for j in range(config.rb_plane_order+1) if i+j <= config.rb_plane_order])
        Y = config.RawaryData.ravel()

        # 最小二乗フィッティング
        coeffs, _, _, _ = np.linalg.lstsq(X, Y, rcond=None)

        # 同じ次元の二次元配列にフィッティング結果を適用
        config.ZaryData = config.RawaryData- (X @ coeffs).reshape(rows, cols)
        

        
    if config.rb_line_type == 0 and config.rb_plane_auto == 0:
            
        config.ZaryData = np.array(config.RawaryData)
        
        
    fitdata = np.zeros_like(config.RawaryData)  # 全ての要素が0の配列を作成する（arraydataと同じ形状）
    tempdata = np.zeros_like(config.RawaryData)

    if config.rb_line_type !=0 :
                
        if config.rb_line_direction == "Horizontal":
                    
            tempdata = np.array(config.RawaryData)
                
        elif config.rb_line_direction == "Vertical":
                    
            tempdata = np.array(config.RawaryData.T)

        if config.rb_line_type == 1: # Polynomianl fitting

            # 各行に対して最小二乗フィッティングを行い、結果を格納する新しい配列を作成する
                     
            fitdata = np.zeros_like(tempdata)  # 全ての要素が0の配列を作成する（arraydataと同じ形状）

            for i, row in enumerate(tempdata):
                x = np.arange(len(row))
                y = row
                coeffs = np.polyfit(x, y, config.rb_line_order)  # order次の最小二乗フィッティングを行う
                fitdata[i] =np.polyval(coeffs, x)  # フィッティング曲線のy値を計算し、fitdataに格納する
        
        elif config.rb_line_type == 2: # median
            
            #二次元配列arraydataの各行ごとに、各列のデータの中央値を二次元配列にして戻す関数。

            fitdata = np.zeros((tempdata.shape[0], tempdata.shape[1]))

            for i, row in enumerate(tempdata):
                median = np.median(row)  # 各行の中央値を計算する
                fitdata[i] = np.full(tempdata.shape[1], median)  # 中央値を各列に入れる


        tempdata -= fitdata

        if config.rb_line_direction == "Horizontal":
                    
            config.ZaryData =tempdata
            
        elif config.rb_line_direction == "Vertical":

            config.ZaryData =tempdata.T
  