import os
import random
import string
import sys

from PIL import Image
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QFileDialog, QFrame,
                             QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton, QStatusBar, QTextEdit,
                             QVBoxLayout, QWidget)


class KeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~
                            Qt.WindowContextHelpButtonHint)

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        duong_dan_icon = os.path.join(bundle_dir, 'icon.ico')
        if os.path.exists(duong_dan_icon):
            self.setWindowIcon(QIcon(duong_dan_icon))

        self.setWindowTitle('Xác thực key')
        self.setFixedSize(420, 900)
        self.setObjectName('key_dialog')

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        tieu_de = QLabel('KÍCH HOẠT PHẦN MỀM')
        tieu_de.setObjectName('tieu_de_dialog')
        tieu_de.setAlignment(Qt.AlignCenter)
        layout.addWidget(tieu_de)

        info_frame = QFrame()
        info_frame.setObjectName('khung_thong_tin_key')
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(10)

        info_title = QLabel('THÔNG TIN CHUYỂN KHOẢN')
        info_title.setObjectName('tieu_de_thong_tin')
        info_layout.addWidget(info_title)

        thong_tin = [
            ('Ngân hàng:', 'Timo Bank'),
            ('Số tài khoản:', '0362961990'),
            ('Chủ tài khoản:', 'TA TUAN ANH')
        ]

        for label, value in thong_tin:
            row = QHBoxLayout()
            label_widget = QLabel(label)
            label_widget.setObjectName('nhan_thong_tin')
            value_widget = QLabel(value)
            value_widget.setObjectName('gia_tri_thong_tin')
            row.addWidget(label_widget)
            row.addWidget(value_widget)
            row.addStretch()
            info_layout.addLayout(row)

        layout.addWidget(info_frame)

        random_key = 'genlinkpro' + \
            ''.join(random.choices(string.ascii_lowercase, k=6))

        qr_frame = QFrame()
        qr_frame.setObjectName('khung_qr')
        qr_layout = QVBoxLayout(qr_frame)
        qr_layout.setContentsMargins(0, 0, 0, 0)

        qr_label = QLabel()
        qr_label.setFixedSize(300, 300)
        qr_label.setAlignment(Qt.AlignCenter)

        qr_url = f'https://img.vietqr.io/image/963388-0362961990-qr_only.png?addInfo={random_key}&accountName=TA+TUAN+ANH'

        qr_pixmap = self.load_image_from_url(qr_url)
        if qr_pixmap:
            size = min(qr_label.width(), qr_label.height())
            scaled_pixmap = qr_pixmap.scaled(
                size, size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            qr_label.setPixmap(scaled_pixmap)

        qr_layout.addWidget(qr_label, 0, Qt.AlignCenter)
        layout.addWidget(qr_frame)

        key_frame = QFrame()
        key_frame.setObjectName('khung_nhap_key')
        key_layout = QVBoxLayout(key_frame)

        key_label = QLabel('Nhập key kích hoạt:')
        key_label.setObjectName('nhan_key')
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText('Nhập key để kích hoạt phần mềm...')
        self.key_input.setObjectName('o_nhap_key')

        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_input)
        layout.addWidget(key_frame)

        ok_button = QPushButton('XÁC NHẬN')
        ok_button.setObjectName('nut_xac_nhan')
        ok_button.setCursor(Qt.PointingHandCursor)
        ok_button.clicked.connect(self.verify_key)
        layout.addWidget(ok_button)

        self.setLayout(layout)
        self.random_key = random_key

        self.setStyleSheet('''
            #key_dialog {
                background-color: #1a1a1a;
            }

            #tieu_de_dialog {
                color: white;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial;
                margin-bottom: 10px;
            }

            #khung_thong_tin_key {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #3d3d3d;
            }

            #tieu_de_thong_tin {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }

            #gia_tri_thong_tin {
                color: #ffffff;
                font-weight: bold;
            }

            #khung_qr {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }


            #khung_nhap_key {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
                border: 1px solid #3d3d3d;
            }

            #nhan_key {
                color: white;
                font-size: 14px;
                font-weight: bold;
                margin-bottom: 5px;
            }

            #o_nhap_key {
                padding: 12px;
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                background-color: #1a1a1a;
                color: white;
                font-size: 14px;
            }

            #o_nhap_key:focus {
                border: 2px solid #ffffff;
                background-color: #2d2d2d;
            }

            #nut_xac_nhan {
                background-color: #ffffff;
                color: #1a1a1a;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 6px;
                margin-top: 10px;
            }

            #nut_xac_nhan:hover {
                background-color: #e0e0e0;
            }

            #nhan_thong_tin {
                color: #ffffff;
                font-size: 14px;
            }
        ''')

    def load_image_from_url(self, url):
        try:
            from urllib.request import urlopen
            data = urlopen(url).read()
            image = QImage()
            image.loadFromData(data)
            return QPixmap(image)
        except Exception:
            return None

    def verify_key(self):
        if self.key_input.text().strip() == self.random_key:
            self.accept()
        else:
            QMessageBox.warning(self, 'Lỗi', 'Key không chính xác!')


class TrinhTaoSEO(QMainWindow):
    def __init__(self):
        super().__init__()
        self.duong_dan_anh = None
        self.check_key()
        self.tao_giao_dien()
        self.ap_dung_style()
        self.thiet_lap_icon()

    def thiet_lap_icon(self):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            bundle_dir = sys._MEIPASS
        else:
            bundle_dir = os.path.dirname(os.path.abspath(__file__))

        duong_dan_icon = os.path.join(bundle_dir, 'icon.ico')
        if os.path.exists(duong_dan_icon):
            self.setWindowIcon(QIcon(duong_dan_icon))

    def tao_giao_dien(self):
        self.setWindowTitle('GENLINK PRO')
        self.setGeometry(100, 100, 600, 450)
        self.setMinimumWidth(500)

        widget_chinh = QWidget()
        self.setCentralWidget(widget_chinh)
        layout_chinh = QVBoxLayout()
        layout_chinh.setSpacing(15)
        layout_chinh.setContentsMargins(20, 20, 20, 20)

        tieu_de = QLabel('GENLINK PRO')
        tieu_de.setObjectName('tieu_de_app')
        layout_chinh.addWidget(tieu_de, 0, Qt.AlignCenter)

        khung_form = QFrame()
        khung_form.setObjectName('khung_form')
        layout_form = QVBoxLayout(khung_form)
        layout_form.setSpacing(15)

        self.tao_phan_tieu_de(layout_form)
        self.tao_phan_mo_ta(layout_form)
        self.tao_phan_chuyen_huong(layout_form)
        self.tao_phan_chon_anh(layout_form)
        self.tao_nut_tao_file(layout_form)

        layout_chinh.addWidget(khung_form)

        self.thanh_trang_thai = QStatusBar()
        self.setStatusBar(self.thanh_trang_thai)

        lien_he = QPushButton('Liên hệ hỗ trợ')
        lien_he.setObjectName('nut_lien_he')
        lien_he.setCursor(Qt.PointingHandCursor)
        lien_he.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl('https://t.me/ovftank')))
        layout_chinh.addWidget(lien_he, 0, Qt.AlignRight)

        widget_chinh.setLayout(layout_chinh)

    def tao_phan_tieu_de(self, layout_cha):
        layout = QHBoxLayout()
        nhan_tieu_de = QLabel('Tiêu đề:')
        self.o_nhap_tieu_de = QLineEdit()
        self.o_nhap_tieu_de.setPlaceholderText('Nhập tiêu đề trang web...')
        layout.addWidget(nhan_tieu_de, 1)
        layout.addWidget(self.o_nhap_tieu_de, 4)
        layout_cha.addLayout(layout)

    def tao_phan_mo_ta(self, layout_cha):
        layout = QHBoxLayout()
        nhan_mo_ta = QLabel('Mô tả:')
        self.o_nhap_mo_ta = QTextEdit()
        self.o_nhap_mo_ta.setPlaceholderText('Nhập mô tả trang web...')
        self.o_nhap_mo_ta.setMaximumHeight(80)
        layout.addWidget(nhan_mo_ta, 1)
        layout.addWidget(self.o_nhap_mo_ta, 4)
        layout_cha.addLayout(layout)

    def tao_phan_chuyen_huong(self, layout_cha):
        layout = QHBoxLayout()
        nhan_url = QLabel('URL:')
        self.o_nhap_url = QLineEdit()
        self.o_nhap_url.setPlaceholderText('https://ovfteam.com')
        layout.addWidget(nhan_url, 1)
        layout.addWidget(self.o_nhap_url, 4)
        layout_cha.addLayout(layout)

    def tao_phan_chon_anh(self, layout_cha):
        layout = QHBoxLayout()

        khung_thong_tin = QFrame()
        khung_thong_tin.setObjectName('khung_thong_tin')
        layout_thong_tin = QVBoxLayout(khung_thong_tin)

        self.nhan_anh = QLabel('Chưa chọn ảnh')
        self.nhan_kich_thuoc = QLabel('Kích thước: -')
        layout_thong_tin.addWidget(self.nhan_anh)
        layout_thong_tin.addWidget(self.nhan_kich_thuoc)

        nut_chon_anh = QPushButton('Chọn Ảnh')
        nut_chon_anh.setObjectName('nut_chon_anh')
        nut_chon_anh.setCursor(Qt.PointingHandCursor)
        nut_chon_anh.clicked.connect(self.chon_anh)

        layout.addWidget(khung_thong_tin, 4)
        layout.addWidget(nut_chon_anh, 1)
        layout_cha.addLayout(layout)

    def tao_nut_tao_file(self, layout_cha):
        nut_tao = QPushButton('Tạo File HTML')
        nut_tao.setObjectName('nut_tao_file')
        nut_tao.setCursor(Qt.PointingHandCursor)
        nut_tao.clicked.connect(self.tao_html)
        layout_cha.addWidget(nut_tao)

    def ap_dung_style(self):
        self.setStyleSheet('''
            QMessageBox {
                background-color: #1a1a1a;
            }

            QMessageBox QLabel {
                color: #ffffff;
                font-size: 13px;
                font-family: 'Segoe UI', Arial;
                padding: 10px;
            }

            QMessageBox QPushButton {
                background-color: #ffffff;
                color: #1a1a1a;
                border-radius: 6px;
                min-width: 80px;
                min-height: 30px;
                font-family: 'Segoe UI', Arial;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 16px;
            }

            QMessageBox QPushButton:hover {
                background-color: #e0e0e0;
            }

            QMainWindow {
                background-color: #1a1a1a;
            }

            #tieu_de_app {
                font-size: 28px;
                font-weight: bold;
                color: white;
                margin-bottom: 20px;
                font-family: 'Segoe UI', Arial;
            }

            #khung_form {
                background-color: #2d2d2d;
                border-radius: 12px;
                padding: 25px;
                border: 1px solid #3d3d3d;
            }

            QLabel {
                color: #ffffff;
                font-weight: 500;
                font-family: 'Segoe UI', Arial;
            }

            QLineEdit, QTextEdit {
                padding: 10px;
                border: 2px solid #3d3d3d;
                border-radius: 6px;
                background-color: #1a1a1a;
                color: white;
                font-size: 13px;
            }

            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #ffffff;
                background-color: #2d2d2d;
            }

            QLineEdit:hover, QTextEdit:hover {
                border: 2px solid #4d4d4d;
            }

            #khung_thong_tin {
                background-color: #1a1a1a;
                border-radius: 6px;
                padding: 15px;
                border: 1px solid #3d3d3d;
            }

            QPushButton {
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                border: none;
                font-size: 13px;
                font-family: 'Segoe UI', Arial;
                min-width: 100px;
            }

            #nut_chon_anh {
                background-color: #ffffff;
                color: #1a1a1a;
            }

            #nut_chon_anh:hover {
                background-color: #e0e0e0;
            }

            #nut_tao_file {
                background-color: #ffffff;
                color: #1a1a1a;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
            }

            #nut_tao_file:hover {
                background-color: #e0e0e0;
            }

            #nut_lien_he {
                background-color: transparent;
                color: #ffffff;
                border: 1px solid #ffffff;
            }

            #nut_lien_he:hover {
                background-color: #ffffff;
                color: #1a1a1a;
            }

            QStatusBar {
                color: #ffffff;
                background-color: #1a1a1a;
                border-top: 1px solid #3d3d3d;
            }

            QStatusBar::item {
                border: none;
            }

            QDialog {
                background-color: #1a1a1a;
            }

            #nut_xac_nhan {
                background-color: #ffffff;
                color: #1a1a1a;
                padding: 12px;
                font-size: 14px;
                font-weight: 600;
            }

            #nut_xac_nhan:hover {
                background-color: #e0e0e0;
            }
        ''')

    def xac_dinh_loai_anh(self, duong_dan_anh):
        try:
            with Image.open(duong_dan_anh) as img:
                format_to_mime = {
                    'JPEG': 'image/jpeg',
                    'PNG': 'image/png',
                    'GIF': 'image/gif',
                    'WEBP': 'image/webp',
                    'BMP': 'image/bmp'
                }
                return format_to_mime.get(img.format, 'image/jpeg')
        except Exception:
            return 'image/jpeg'

    def tao_noi_dung_html(self, ten_anh, chieu_rong, chieu_cao):
        image_type = self.xac_dinh_loai_anh(self.duong_dan_anh)

        return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.o_nhap_tieu_de.text()}</title>

    <meta name="description" content="{self.o_nhap_mo_ta.toPlainText()}">
    <meta name="image" content="/{ten_anh}">
    <meta name="keywords" content="{self.o_nhap_tieu_de.text()}">
    <meta name="robots" content="index, follow">

    <meta property="og:type" content="article">
    <meta property="og:title" content="{self.o_nhap_tieu_de.text()}">
    <meta property="og:description" content="{self.o_nhap_mo_ta.toPlainText()}">
    <meta property="og:image" content="/{ten_anh}">
    <meta property="og:image:url" content="/{ten_anh}">
    <meta property="og:image:type" content="{image_type}">
    <meta property="og:image:width" content="{chieu_rong}">
    <meta property="og:image:height" content="{chieu_cao}">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{self.o_nhap_tieu_de.text()}">
    <meta name="twitter:description" content="{self.o_nhap_mo_ta.toPlainText()}">
    <meta name="twitter:image" content="/{ten_anh}">

    <script>
        function detectBot() {{
            const botPatterns = [
                'bot', 'spider', 'crawl', 'slurp', 'facebook', 'whatsapp',
                'telegram', 'viber', 'twitter', 'discord', 'slack',
                'linkedin', 'skype', 'pinterest', 'zoom'
            ];

            const userAgent = navigator.userAgent.toLowerCase();

            if (botPatterns.some(pattern => userAgent.includes(pattern))) {{
                return true;
            }}

            if (navigator.webdriver || window.navigator.webdriver) {{
                return true;
            }}

            const automationTools = [
                '_phantom',
                '__nightmare',
                'callPhantom',
                'buffer',
                'awesomium',
                'cef',
                'selenium',
                'headless',
                'phantomjs',
                'nightmarejs',
                'rhino'
            ];

            for (const tool of automationTools) {{
                if (window[tool]) {{
                    return true;
                }}
            }}

            if (navigator.plugins.length === 0) {{
                return true;
            }}

            return false;
        }}

        window.onload = function() {{
            if (!detectBot()) {{
                window.location.replace("{self.o_nhap_url.text()}");
            }} else {{
                document.getElementById('content').style.display = 'block';
            }}
        }};
    </script>
</head>
<body>
    <div id="content" style="display: none">
        <h1>{self.o_nhap_tieu_de.text()}</h1>
        <img src="{ten_anh}" alt="{self.o_nhap_tieu_de.text()}" width="{chieu_rong}" height="{chieu_cao}">
        <p>{self.o_nhap_mo_ta.toPlainText()}</p>
    </div>
</body>
</html>"""

    def chon_anh(self):
        ten_file, _ = QFileDialog.getOpenFileName(
            self,
            'Chọn Ảnh',
            '',
            'File Ảnh (*.png *.jpg *.jpeg *.gif *.bmp)'
        )
        if ten_file:
            self.duong_dan_anh = ten_file
            ten_anh = os.path.basename(ten_file)
            self.nhan_anh.setText(f'Tên file: {ten_anh}')

            with Image.open(ten_file) as anh:
                chieu_rong, chieu_cao = anh.size
                self.nhan_kich_thuoc.setText(
                    f'Kích thước: {chieu_rong}x{chieu_cao}px')

            self.thanh_trang_thai.showMessage('Đã chọn ảnh thành công!', 3000)

    def tao_html(self):
        if not self.duong_dan_anh:
            self.thanh_trang_thai.showMessage('Vui lòng chọn ảnh trước!', 3000)
            return

        if not self.o_nhap_tieu_de.text().strip():
            self.thanh_trang_thai.showMessage('Vui lòng nhập tiêu đề!', 3000)
            return

        if not self.o_nhap_url.text().strip():
            self.thanh_trang_thai.showMessage(
                'Vui lòng nhập URL chuyển hướng!', 3000)
            return

        try:
            os.makedirs('output', exist_ok=True)

            with Image.open(self.duong_dan_anh) as anh:
                chieu_rong, chieu_cao = anh.size

            ten_anh = os.path.basename(self.duong_dan_anh)
            duong_dan_anh_moi = os.path.join('output', ten_anh)
            with open(self.duong_dan_anh, 'rb') as src, open(duong_dan_anh_moi, 'wb') as dst:
                dst.write(src.read())

            noi_dung_html = self.tao_noi_dung_html(
                ten_anh, chieu_rong, chieu_cao)
            with open('output/index.html', 'w', encoding='utf-8') as f:
                f.write(noi_dung_html)

            self.thanh_trang_thai.showMessage(
                'Đã tạo file thành công! Kiểm tra thư mục output.', 5000)

            msg_box = QMessageBox(self)
            msg_box.setWindowTitle('Thành công')
            msg_box.setText('Đã tạo file thành công!')
            msg_box.setInformativeText(
                'Bạn có muốn mở thư mục chứa file không?')
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.Yes)

            msg_box.button(QMessageBox.Yes).setCursor(Qt.PointingHandCursor)
            msg_box.button(QMessageBox.No).setCursor(Qt.PointingHandCursor)

            msg_box.button(QMessageBox.Yes).setText('Mở thư mục')
            msg_box.button(QMessageBox.No).setText('Đóng')

            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                icon_dir = sys._MEIPASS
            else:
                icon_dir = os.path.dirname(os.path.abspath(__file__))

            msg_box.setIconPixmap(QIcon(os.path.join(
                icon_dir, 'icon.ico')).pixmap(32, 32))

            reply = msg_box.exec_()

            if reply == QMessageBox.Yes:
                duong_dan_output = os.path.abspath('output')
                QDesktopServices.openUrl(QUrl.fromLocalFile(duong_dan_output))

        except Exception as e:
            self.thanh_trang_thai.showMessage(f'Lỗi: {str(e)}', 5000)

    def check_key(self):
        appdata_path = os.path.join(os.getenv('APPDATA'), 'GenLinkPro')
        key_file = os.path.join(appdata_path, 'key.txt')

        if os.path.exists(key_file):
            try:
                with open(key_file, 'r') as f:
                    saved_key = f.read().strip()
                if saved_key and saved_key.startswith('genlinkpro'):
                    self.tao_giao_dien()
                    self.ap_dung_style()
                    self.thiet_lap_icon()
                    return
            except Exception:
                pass

        dialog = KeyDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                os.makedirs(appdata_path, exist_ok=True)
                with open(key_file, 'w') as f:
                    f.write(dialog.random_key)
            except Exception as e:
                print(f"Lỗi khi lưu key: {e}")

            self.tao_giao_dien()
            self.ap_dung_style()
            self.thiet_lap_icon()
        else:
            sys.exit()


def main():
    app = QApplication(sys.argv)
    chuong_trinh = TrinhTaoSEO()
    chuong_trinh.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
