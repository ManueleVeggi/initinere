import tabula
import pandas

def scraper(uri, page, exportName):
    table = tabula.read_pdf(uri,pages=page)
    table[0].to_excel(exportName)
    return True

source = "https://www.istat.it/it/files/2016/11/Studenti-e-bacini-universitari.pdf"
destination = "data/scraping/averageincomeRawp2.xlsx"

print(scraper(source, 38, destination))
