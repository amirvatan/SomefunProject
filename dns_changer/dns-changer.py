from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import sys , os , subprocess , re
from pathlib import Path
class dnschanger(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.dns_lists = QComboBox()
        self.dns_name = QLineEdit()
        self.dns_input1 = QLineEdit()
        self.dns_input2 = QLineEdit()
        self.status = QLabel()
        self.save_btn = QPushButton("Save")
        self.start_btn = QPushButton("Start Dns")
        self.stop_btn = QPushButton("Stop Dns")
        self.checkping_btn = QPushButton("Check ping")
        self.remove_btn = QPushButton("Remove")
        username = os.environ.get('SUDO_USER', os.environ.get('USERNAME'))
        self.home_path = os.path.expanduser(f'~{username}')
        
        self.initUI()
    def initUI(self):
      
        btn_layout = QHBoxLayout()
        btn_layout2 = QHBoxLayout()
        input_layout = QHBoxLayout()
        dns_layout = QHBoxLayout()
        stop_layout = QHBoxLayout()
       
       
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.start_btn)
        btn_layout2.addWidget(self.checkping_btn)
        btn_layout2.addWidget(self.remove_btn)
        
        
        
        
        
        
        dns_layout.addWidget(self.dns_lists)
        dns_layout.setContentsMargins(0,0,0,25)
        
        
        self.dns_input1.setInputMask('999.999.999.999')
        
        self.dns_input2.setInputMask('999.999.999.999')
        input_layout.addWidget(self.dns_input1)
        input_layout.addWidget(self.dns_input2)
        input_layout.addWidget(self.dns_name)
        input_layout.setContentsMargins(0,0,0,25)
        
        
        stop_layout.addWidget(self.stop_btn)
        
        form_btn = QFormLayout()
        
        form_btn.addRow(dns_layout)
     
        form_btn.addRow(input_layout)
        form_btn.addRow(btn_layout)
        form_btn.addRow(btn_layout2)
        form_btn.addRow(stop_layout)
        form_btn.addWidget(self.status)
        
        
        self.setLayout(form_btn)
    def getdata(self):
        self.dns_lists.clear()
        try:
            with open(f'{self.home_path}/.config/dns_changer/conf', 'r') as conf_file:
                data = conf_file.read().split('\n')
                
                for line in data: 
                    if len(line.split(' ')) < 2:
                        continue
                    subs = line.split(' ')
                    
                    self.dns_lists.addItem(subs[0])
                    self.dns_input1.setText(subs[1])
                    self.dns_input2.setText(subs[2])
                self.dns_lists.setCurrentText(subs[0])
                self.dns_name.setText(subs[0])
        except:
            self.save_file(create_file = True)
                    
    
    def dns_change(self,argv):
       
        with open(f'{self.home_path}/.config/dns_changer/conf', 'r') as conf_file:
            data = conf_file.read().split('\n')
                    
              
            for line in data: 
                if len(line.split(' ')) < 2:
                    continue
                subs = line.split(' ')
                if subs[0] == self.dns_lists.currentText():
                    self.dns_input1.setText(subs[1])
                    self.dns_input2.setText(subs[2])
                    self.dns_name.setText(subs[0])
                    
            self.status.setText('Dns changed')

    def save_file(self,create_file= False):
        dns_name = self.dns_name.text()
        prime_dns = self.dns_input1.text()
        second_dns = self.dns_input2.text()

        if create_file:
             dns_name = 'google'
             prime_dns = '8.8.8.8'
             second_dns = '8.8.4.4'
    
        if create_file == False:
            with open(f'{self.home_path}/.config/dns_changer/conf', 'r+') as conf_file:
                data = conf_file.readlines()
                conf_file.seek(0)
                for line in data:
                    if line.split(' ')[0] != dns_name:
                        conf_file.write(line)
                conf_file.write(f'{dns_name} {prime_dns} {second_dns}\n')
                conf_file.truncate()
                
                
               
               
            # with open(f'{self.home_path}/.config/dns_changer/conf', 'a') as conf_file:
                
                        
            #     conf_file.write(f'{dns_name} {prime_dns} {second_dns}\n')
            #     self.getdata()  
        else :
            with open(f'{self.home_path}/.config/dns_changer/conf', 'w') as conf_file:
                
                        
                conf_file.write(f'{dns_name} {prime_dns} {second_dns}\n')
                conf_file.close()
        self.getdata()
            
    def dns_remove(self):
     
        try:
            with open(f'{self.home_path}/.config/dns_changer/conf', 'r+') as conf_file:
                    data = conf_file.readlines()
                    conf_file.seek(0)
                    for line in data:
                    
                        if line.split(' ')[0] != self.dns_name.text():
                        
                            conf_file.write(line)
                
                    conf_file.truncate()
                    self.getdata()
        except:
            self.status.setText('there is no dns config to remove')
                       
    def dns_start(self):
        prime_dns = self.dns_input1.text()
        second_dns = self.dns_input2.text()
        
        with open(f'/etc/resolv.conf.head', 'w') as conf_file:
                conf_file.write(f'nameserver {prime_dns}\n')
                conf_file.write(f'nameserver {second_dns}\n')
        os.system('sudo dhcpcd -n')
    
    def dns_stop(self):
        with open(f'/etc/resolv.conf.head', 'w') as conf_file:
            conf_file.write('')
            
        os.system('sudo dhcpcd -n')        
        
    def dns_checkping(self):
        prime_dns = self.dns_input1.text()
        second_dns = self.dns_input2.text()
        ping1 = subprocess.check_output(f'ping -w 3 -q {prime_dns} | cut -d "/" -s -f5', shell = True)
        ping2 = subprocess.check_output(f'ping -w 3 -q {second_dns} | cut -d "/" -s -f5', shell = True)
        ping1 = re.split('\D', str(ping1))[2]
        ping2 = re.split('\D', str(ping2))[2]
        self.status.setText(f'first : {ping1}, second : {ping2}')
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    
    win = dnschanger()
    win.getdata()
    win.dns_lists.activated[str].connect(win.dns_change)
    win.save_btn.clicked.connect(win.save_file)
    win.remove_btn.clicked.connect(win.dns_remove)
    win.start_btn.clicked.connect(win.dns_start)
    win.stop_btn.clicked.connect(win.dns_stop)
    win.checkping_btn.clicked.connect(win.dns_checkping)
    win.resize(500, 200)
    win.move(100, 100)
          
        
    win.show()
    sys.exit(app.exec_())
        