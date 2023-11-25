from PyQt5.QtCore import QThread, pyqtSignal
import mint  # Add this line to import the 'mint' module

class MintingThread(QThread):
    mint_complete = pyqtSignal(str)

    def __init__(self, selected_rpc_value, private_key, dataHex, quantity):
        super().__init__()
        self.mints = mint.EVM_Minter(selected_rpc_value, private_key, dataHex)
        self.quantity = quantity

    def run(self):
        try:
            for _ in range(int(self.quantity)):
                result = self.mints.mint()
                if result is not None and isinstance(result, str):
                    self.mint_complete.emit(result)
            self.mint_complete.emit("铸造完成......")
        except Exception as e:
            self.mint_complete.emit(f"报错信息如下：\nException occurred: {str(e)}")
