from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
import minting_thread as mt

class Main_WIN(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 创建选择节点的下拉列表和标签
        rpc_label = self.createCheckBox()

        # 创建输入铸造数量的标签和文本框
        quantity_label = QLabel('输入铸造数量:')
        self.quantity_input = QLineEdit(self)

        # 创建输入私钥的标签和文本框
        private_key_label = QLabel('输入私钥:')
        self.private_key_input = QLineEdit(self)

        # 创建铸造铭文的标签和文本框
        dataHex = QLabel('铸造铭文:')
        self.dataHex = QLineEdit(self)

        # 创建提交按钮
        submit_button = QPushButton('开始铸造', self)
        submit_button.clicked.connect(self.submitClicked)

        # 创建结束按钮
        stop_button = QPushButton('结束', self)
        stop_button.clicked.connect(self.stopClicked)

        # 设置整个窗口的字体大小为10
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        # 水平布局1：选择节点和铸造数量在同一行
        hbox_layout1 = QHBoxLayout()
        hbox_layout1.addWidget(rpc_label)
        hbox_layout1.addWidget(self.rpc_combo_box)  # 添加下拉列表框
        hbox_layout1.addWidget(quantity_label)
        hbox_layout1.addWidget(self.quantity_input)

        # 水平布局2：输入私钥在新的一行
        hbox_layout2 = QHBoxLayout()
        hbox_layout2.addWidget(private_key_label)
        hbox_layout2.addWidget(self.private_key_input)  # 添加私钥输入框

        # 水平布局3：铸造铭文在新的一行
        hbox_layout3 = QHBoxLayout()
        hbox_layout3.addWidget(dataHex)
        hbox_layout3.addWidget(self.dataHex)  # 添加铸造铭文输入框

        # 水平布局4：开始铸造和结束按钮在同一行
        hbox_layout4 = QHBoxLayout()
        hbox_layout4.addWidget(submit_button)
        hbox_layout4.addWidget(stop_button)


        # 竖直布局
        vbox_layout = QVBoxLayout()
        vbox_layout.addLayout(hbox_layout1)
        vbox_layout.addLayout(hbox_layout2)
        vbox_layout.addLayout(hbox_layout3)
        vbox_layout.addLayout(hbox_layout4)

        # 创建用于显示输出信息的文本框
        self.output_text_edit = QPlainTextEdit(self)
        self.output_text_edit.setReadOnly(True)  # 设置为只读，防止用户编辑文本
        vbox_layout.addWidget(self.output_text_edit)

        self.setLayout(vbox_layout)

        self.setWindowTitle('evm批量铸造')
        self.setGeometry(600, 600, 600, 600)

    def submitClicked(self):
        # 获取选择的节点的名称和值
        selected_rpc_name = self.rpc_combo_box.currentText()
        selected_rpc_value = self.rpc_combo_box.currentData()
        quantity = self.quantity_input.text()
        private_key = self.private_key_input.text()
        dataHex = self.dataHex.text()


        if not private_key :
            QMessageBox.warning(self, '警告', '请输入私钥！', QMessageBox.Ok)
            return

        if not dataHex :
            QMessageBox.warning(self, '警告', '请输入铸造的16进制数据！', QMessageBox.Ok)
            return

        # 在输出文本框中显示信息
        self.output_text_edit.appendPlainText("开始铸造........")

        
        try:
            self.mint_thread = mt.MintingThread(selected_rpc_value, private_key, dataHex, quantity)
            self.mint_thread.mint_complete.connect(self.handleMintSignal)
            self.mint_thread.start()
        except Exception as e:
            self.output_text_edit.appendPlainText("报错信息如下：")
            self.output_text_edit.appendPlainText(f"Exception occurred: {str(e)}")

    def handleMintSignal(self, message):
        self.output_text_edit.appendPlainText(message)

    def stopClicked(self):
        # 处理结束按钮点击事件，你可以在这里添加结束操作的逻辑
        self.output_text_edit.appendPlainText("铸造结束")

    def createCheckBox(self):
        # 创建下拉列表和标签
        rpc_label = QLabel('选择RPC节点:')
        self.rpc_combo_box = QComboBox(self)
        self.rpc_combo_box.addItem('马蹄节点', "https://polygon.llamarpc.com")  # 设置节点名称和对应的值
        self.rpc_combo_box.addItem('币安节点', "https://binance.llamarpc.com")
        self.rpc_combo_box.addItem('以太节点', "https://eth.llamarpc.com")
        self.rpc_combo_box.addItem('Base节点', "https://base.llamarpc.com")
        self.rpc_combo_box.addItem('AVAX节点', "https://avax-pokt.nodies.app/ext/bc/C/rpc")
        self.rpc_combo_box.addItem('OP节点', "https://optimism.llamarpc.com")
        self.rpc_combo_box.addItem('ARB节点', "https://arbitrum.llamarpc.com")
        return rpc_label

if __name__ == '__main__':
    app = QApplication([])
    main_win = Main_WIN()
    main_win.show()
    app.exec_()
