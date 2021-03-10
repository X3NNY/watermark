# -*- coding: utf-8
import reportlab.pdfbase.ttfonts
import platform
import argparse
import PyPDF2
import sys
import os

from reportlab.lib.units import cm
from reportlab.pdfgen import canvas

# Windows
# Darwin
# Linux
system = platform.system()

parser = argparse.ArgumentParser(description="Watermark for PDF")
parser.add_argument('watermark', metavar='watermark', type=str, nargs='?', default='Powered By X3NNY')
parser.add_argument('-p', '--path', dest='path', type=str, required=True, help='Add all if path is a directory')
parser.add_argument('-d', '--depth', dest='depth', type=int, default=1, help='The traversal depth（default 1）')
parser.add_argument('-o', '--outpt', dest='output', type=str, default=None, help='The ouput path of watermark file (default .)')
parser.add_argument('-k', '--keep-structure', dest='ks', action='store_const', default=False, const=True, help="Keep the folder structure if exists")

parser.add_argument('-s', '--suffix', dest='suffix', type=str, default='-水印')


args = parser.parse_args()

path: str = args.path
wm: str = args.watermark
is_file: bool = os.path.isfile(path)
depth: int = args.depth
output: str = os.getcwd() if args.output is None else (args.output if args.output != '@' else (os.path.dirname(path) if is_file else path))
suffix: str = '' if args.suffix == '@' else args.suffix
ks = args.ks

sc = 0
fc = 0

if not is_file and not os.path.isdir(path):
    print("[?] %s: No such file or directory" % path)
    exit(-2)

if not os.path.exists(output) or not os.path.isdir(output):
    print("[?] %s: No such directory or does not exist")
    exit(-3)

print('[*] Starting!')
print('[*] Author: X3NNY')
print('[*] GitHUB: https://github.com/X3NNY/watermark')

class config_class:
    def __init__(self):
        self.width = 21
        self.height = 29.7
        self.ratio = self.height / self.width
        self.color = (0, 0, 0)
        self.alpha = 0.1
        self.rotate = 40
        self.font_size = 45
        self.file_name = "watermark_temp.pdf"

config = config_class()

def init_config():
    pass


def gen_watermark_pdf(wm: str, config: config_class):
    """Generate a watermark pdf

    Args:
        wm (str): [watermark content]
        config (config_class): [config]
    """
    file_name = config.file_name
    c = canvas.Canvas(file_name, pagesize=(config.width*cm, config.height*cm))
    c.translate(10*cm, 0*cm)

    if system == 'Darwin':
        font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
    elif system == 'Windows':
        font_path = 'C:/Windows/Fonts/simhei.ttf'

    try:
        reportlab.pdfbase.pdfmetrics.registerFont(
            reportlab.pdfbase.ttfonts.TTFont('heiti', font_path)
        )
        c.setFont('heiti', config.font_size)
    except:
        c.setFont('Helvetica', config.font_size)
    
    c.rotate(config.rotate)
    c.setFillColorRGB(*config.color)
    c.setFillAlpha(config.alpha)
    for i in range(-2*wm.__len__(), round(config.width), 2*wm.__len__()):
        for j in range(-6, round(config.height), 6):
            c.drawString(i*cm, j*cm, wm)
    c.save()
    return file_name

def add_watermark(file_in: str, file_mark: str, file_out: str):
    global sc, fc
    try:
        pdf_out = PyPDF2.PdfFileWriter()
        pdf_in = PyPDF2.PdfFileReader(open(file_in, 'rb'), strict=False)
        pdf_mark = PyPDF2.PdfFileReader(open(file_mark, 'rb'), strict=False)
        
        for i in range(pdf_in.numPages):
            page = pdf_in.getPage(i)
            page.mergePage(pdf_mark.getPage(0))
            page.compressContentStreams()
            pdf_out.addPage(page)
        pdf_out.write(open(file_out, 'wb+'))
        sc += 1
        print('[+] Create %s success.' % file_out)
    except:
        fc += 1
        print('[-] Create %s fail.' % file_out)
    

mark_name = gen_watermark_pdf(wm, config)
print('[+] Create watermark temporary pdf file')

def add_dir(sub_path: str):
    """Add watermark for a diretory

    Args:
        sub_path (str): [path]
    """
    for file_name in os.walk(os.path.join(path, sub_path)).__next__()[2]:
            file_name = os.path.basename(file_name)
            if file_name.split('.')[-1] == 'pdf' and file_name != mark_name and file_name.find(suffix) == -1:
                file_path = os.path.join(path, sub_path, file_name)
                output_path = "%s%s.pdf" % (os.path.basename('.'.join(file_path.split('.')[:-1])), suffix)
                if ks:
                    output_path = os.path.join(output, sub_path, output_path)
                else:
                    output_path = os.path.join(output, output_path)
                add_watermark(file_path, mark_name, output_path)

def work():
    global path, depth, output
    if is_file:
        output_path = "%s%s.pdf" % (os.path.basename('.'.join(path.split('.')[:-1])), suffix)
        output_path = os.path.join(output, output_path)
        add_watermark(path, mark_name, output_path)
    else:
        path_list = ['./']
        while depth > 0:
            tmp_list = []
            for p in path_list:
                add_dir(p)
            
            if depth == 1:
                break

            depth -= 1
            for sub_path in path_list:
                for sub_dir in os.listdir(os.path.join(path, sub_path)):
                    if sub_dir.startswith('.') or not os.path.isdir(os.path.join(path, sub_path,sub_dir)):
                        continue
                    tmp_path = os.path.join(sub_path,sub_dir)
                    if ks and not os.path.exists(os.path.join(output, tmp_path)):
                        os.mkdir(os.path.join(output, tmp_path))
                        print('[+] Create directory %s success.' % os.path.join(output, tmp_path))
                    if os.path.isdir(tmp_path):
                        tmp_list.append(tmp_path)
            
            path_list = tmp_list
    os.remove(mark_name)
    print('[-] Remove watermark temporary pdf file.')

if __name__ == "__main__":
    try:
        work()
        print('[*] Found %d file(s), %d successed and %d failed.' % (sc+fc, sc, fc))
        print('[*] Watermark work done. Successful!')
    except BaseException as e:
        print(e)
        print('[*] Found %d file(s), %d successed and %d failed.' % (sc+fc, sc, fc))
        print('[!] Something error.. maybe u should check the path')