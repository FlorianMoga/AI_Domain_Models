from Model.Photo import Photo

if __name__ == '__main__':
    original_invoice = Photo(r"C:\Users\Florian Moga\Desktop\GEP\Invoice Florian Moga 2208883908600452-1.jpg")
    #original_invoice.show_img()

    #print(original_invoice.get_characters_middlepoint()[0])
    #print(original_invoice.define_clusters())

    original_invoice.draw_all_segments()
    original_invoice.show_img()