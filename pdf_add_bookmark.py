from PyPDF2 import PdfReader, PdfWriter
import re
import numpy as np
import argparse


def read_bmk(bmk_path):
    bmk_file = open(bmk_path,'r')
    list_bmk = []
    
    while 1:
        bmk_file_i = bmk_file.readline()
        if bmk_file_i == "":
            break
        bmk_page = int(re.findall("\d+",bmk_file_i)[-1]) - 1
        bmk_reverse = bmk_file_i[::-1]
        bmk_reverse_title_space = bmk_reverse.split(" ", 1)[-1]
        bmk_reverse_title = bmk_reverse_title_space[::-1].rstrip()
        bmk_tab_sub_bmk = bmk_reverse_title.count(" ") - bmk_reverse_title.strip().count(" ")
        list_bmk.append([bmk_reverse_title.strip(), bmk_page, bmk_tab_sub_bmk])

    list_bmk = np.array(list_bmk, dtype=object)
    list_bmk[:, -1] = list_bmk[:, -1] // np.gcd.reduce(list_bmk[:, -1])
    return list_bmk


def write_bmk(pdf_path, bmk_info, pdf_output):
    pdf = open(pdf_path, "rb")
    reader = PdfReader(pdf)
    n_pages = reader._get_num_pages()
    pages = range(n_pages)
    
    writer = PdfWriter()
    for page in pages:
        writer.add_page(reader.pages[page])
        
    bmk_parent = []

    for bmk in bmk_info:
        bmk_status = len(bmk_parent) - bmk[-1]
        if bmk[-1] == 0:
            parent = writer.add_outline_item(bmk[0], bmk[1])
            bmk_parent = [parent]
            
        elif bmk_status == 0:
            parent = writer.add_outline_item(bmk[0], bmk[1], parent=bmk_parent[bmk[-1]-1])
            bmk_parent.append(parent)
            
        elif bmk_status == 1:
            parent = writer.add_outline_item(bmk[0], bmk[1], parent=bmk_parent[bmk[-1]-1])
            bmk_parent[-1] = parent
            
        elif bmk_status > 1:
            parent = writer.add_outline_item(bmk[0], bmk[1], parent=bmk_parent[bmk[-1]-1])
            for i in range(bmk_status-1):
                bmk_parent.pop(-1)
            bmk_parent[-1] = parent

    with open(pdf_output, "wb") as fp:
        writer.write(fp)


def main_bmk(path_in, bmk, path_out=None, replace_input=False):
    bmk_info = read_bmk(bmk)
    if replace_input:
        write_bmk(path_in, bmk_info, path_in)
    else:
        write_bmk(path_in, bmk_info, path_out)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pi', '--path_in', type=str, help='pdf path input')
    parser.add_argument('-b', '--bmk', type=str, help='bookmark file')
    parser.add_argument('-po', '--path_out', type=str, default=None, help='pdf path output')
    parser.add_argument('-r', '--replace_input', default=False, action='store_true', help='replace to pdf input')
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    # opt = parse_opt()
    # main_bmk(**vars(opt))
    pdf = r"C:\Users\Lenovo\Desktop\my_python\C++ slide.pdf"
    bmk = r"C:\Users\Lenovo\Desktop\my_python\C++_slide.bmk"
    main_bmk(pdf, bmk, replace_input=True)