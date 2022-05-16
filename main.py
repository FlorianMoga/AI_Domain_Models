from Model.Photo import Photo

if __name__ == '__main__':
    file = r"C:\Users\Florian Moga\Desktop\GEP\Invoice Florian Moga 2208883908600452-1.jpg"
    original_invoice = Photo(file)

    cluster_coords = original_invoice.define_clusters()
    original_invoice.draw_all_segments(cluster_coords)
    #original_invoice.show_img()