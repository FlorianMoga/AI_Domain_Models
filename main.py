import json
from Model.Photo import Photo
from Model.TextProcessing import TextProcessing

if __name__ == '__main__':
    acces_token = \
        'eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJBY3Rpdml0aWVzIjoiIiwiR3JvdXBzIjoiYWVlMWI1MGQtM2QxYi00MDg4LWJjOWEtODBlNWIxM2U4MGM1LDJhOGY4ZjZjLWRmNDItNGU3Ny04YjRhLTM2MWY5YmMyZjFlMixmMGY5ZTUwYi0xNGFjLTRjYzItYmU0ZS01MTc3NjdkZjFiNjEsOTNlNmVkYjAtNDVlOC00NTg5LWE2ZmEtMjJkOTM5MDYwYWZjLDY4OTJkNzQ3LTQ2YmMtNDc4OC1hNGIxLWNkODc4ZGM2MzY0YyxkZWRlMDI5Mi1lMTYwLTRjOGYtYTc3Mi0zMjRlZWVkYzM3NjcsNzIzM2NlMTUtMjkyNS00ZTVhLTliYjMtNDBhMjZmOTY0YjBjLGUyZDczMWJhLTA5N2QtNDJiMi04MDliLTJlZTkwOGE4NmJlNyxkNzQ1ZTliMi0yZjdjLTQ3Y2YtYmYwNS02MzljMzBlMjE2ZTAsMDI4ODBhMGUtZWU2NS00ZjU0LWFjYzgtNTBkNTgwNmNkNmE3LDBiYWMyNDc5LTVjNzMtNGRiMC1iY2RkLTBjMDZhY2I5NjhmOCw1ZDdmZDBjMy1hMWU1LTQyZGUtODQ5MC0yZjgxYjU5YjRjYjcsNDBjM2NiOWQtMDc5OS00ZTJhLTllMTEtYzZkNGY1ZTdiYzMxLDViZDUzZjZmLWJkNmQtNGI2NS05Njk5LTE1ZDk4NDY0MzcyYSwyYjExMGIyNS01ZWZmLTRlN2UtOTkzOC04YWRhMGJiMTVmNjUsZjRjOTViMTctNmQ1ZC00NGNkLTgzMWUtMzI3NWI0M2NkMDEyLDgyZTgzZjg4LWU4OWMtNDg3Yi1hMzY5LWZjMzE0MzM4MGU0OSwxMzNkNWEyNS0xOGExLTRiZTMtOTJjZC0xMTk2MDg0NTcxMDUsNzg5OTFmYWItOWRhZS00ZTc4LWI5OTYtYjE0ZjBmOTI5ZThhLDU2ZTUwNDQ2LTFhMGUtNGY2NC04NTgyLWMxYzNhOWVkYmE1YyIsInVuaXF1ZV9uYW1lIjoiSW9udXQuTWloYWlAZ2VwLmNvbSIsImV4cCI6MTY1NjU5NTg1MCwiaXNzIjoiaHR0cHM6Ly9wbGF0Zm9ybWRldi5nZXAuY29tLyIsImF1ZCI6Imh0dHBzOi8vcGxhdGZvcm1kZXYuZ2VwLmNvbS8ifQ.Ubmk5gVjedNEu6MucIcCgydufyCxZGQaMvqNKhAomVI'

    # gep_table = [79, 549, 920, 971]
    # file = r'Invoices/CXN904KL.jpg'

    gep_ph = [121, 542, 868, 914]
    file = r'Invoices/CXN904KL_Photo.png'

    # dell = [51, 629, 963, 829]
    # file = r'Invoices/K0AC99Q.png'

    # inv_table = [88, 548, 917, 1071]
    # bolt_table = [58, 485, 944, 563]

    # file = r"C:\Users\Florian Moga\Desktop\GEP\Rechnung-12000032162-VR130027438-1.jpg"
    # file = r'C:\Users\Florian Moga\Desktop\GEP\Invoice Florian Moga 2208883908600452-1.jpg'

    original_invoice = Photo(file)
    original_invoice.set_table(gep_ph)
    original_invoice.define_clusters()
    original_invoice.associate_clusters()
    original_invoice.draw_all_segments()
    original_invoice.save_processed()
    # original_invoice.show_img()

    text = original_invoice.get_text_from_segments()

    process_text = TextProcessing(text)
    nameJSON = process_text.createJSON('JSON/structure.json')

    with open('JSON/' + nameJSON) as json_file:
        myJSON = json.load(json_file)

    process_text.set_dictionary(myJSON)
    # process_text.createRequestGEP(acces_token)
