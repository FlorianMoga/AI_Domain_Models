from .Model.Photo import Photo
from .Model.Rectangle import Rectangle

import re

def extract_text(img, table_corners):
    inv_table = [88, 548, 917, 1071]
    bolt_table = [58, 485, 944, 563]

    #file = r"C:\Users\Florian Moga\Desktop\GEP\Rechnung-12000032162-VR130027438-1.jpg"
    #file = fpath
    # file = r'C:\Users\Florian Moga\Desktop\GEP\Rechnung-12000032162-VR130027438-1.jpg'
    # file = r'C:\Users\Florian Moga\Desktop\GEP\Invoice Florian Moga 2208883908600452-1.jpg'
    original_invoice = Photo(img)
    original_invoice.set_table(table_corners)
    original_invoice.define_clusters()
    original_invoice.associate_clusters()

    '''text = original_invoice.get_text_from_segments()

    text_file = open(r'C:\Workspace\Python\GEP\inv_text', "w")

    for segment in text:
        text_file.write(segment)
        text_file.write('---')
        text_file.write('\n')

    # close file
    text_file.close()'''

    #original_invoice.draw_all_segments()
    #original_invoice.show_img()
