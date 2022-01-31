from io import BytesIO
import os
import img2pdf
import re
from os import walk
from os.path import join
import requests
from bs4 import BeautifulSoup

CURRENT = os.path.dirname(__file__)


class SlideShareDownloader:
    """SlideShare Downloader Class"""

    def get_slide_info(self, url):
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        title = soup.find(class_='j-title-breadcrumb').get_text().strip()
        image_url = soup.find(class_='slide-image')['srcset']
        final_img_url = image_url.split(',')[2].replace(' ','').replace('1024w','')
        total_slides = soup.find(id='total-slides').get_text().strip()
        metadata = soup.find_all(class_='metadata-item')
        category, date, views = None, None, None
        if len(metadata) >= 3:
            category, date, views = metadata[0].get_text().strip(
            ), metadata[1].get_text().strip(), metadata[2].get_text().strip()

        return title, final_img_url, total_slides, category, date, views

    def get_pdf_name(self, url):
        # get url basename and replace non-alpha with '_'
        pdf_f = re.sub('[^0-9a-zA-Z]+', '_', url.split("/")[-1])
        if pdf_f.strip() == '':
            print("Something wrong to get filename from URL, fallback to result.pdf")
            pdf_f = "result.pdf"
        else:
            pdf_f += ".pdf"
        return pdf_f

    def download_images(self, slideshare_url):
        html = requests.get(slideshare_url).content
        soup = BeautifulSoup(html, 'lxml')
        # soup.title.string
        title = '/tmp'
        images = soup.findAll('img', {'class': 'slide-image'})
        i = 0
        for image in images:
            image_url = image.get('src')
            final_img_url = image_url.split(',')[2].replace(' ', '').replace('1024w', '')
            img = requests.get(final_img_url, verify=False)
            if not os.path.exists(title):
                os.makedirs(title)
            with open(f"{title}/{i}", 'wb') as f:
                f.write(img.content)
            i += 1

        bfr, filename = self.convert_to_pdf(
            title, self.get_pdf_name(slideshare_url))
        return bfr, filename

    def convert_to_pdf(self, img_dir_name, pdf_file_name):
        try:
            f = []
            for (dirpath, dirnames, filenames) in walk(join(CURRENT, img_dir_name)):
                f.extend(filenames)
                break
            f = ["%s/%s" % (img_dir_name, x) for x in f]

            def atoi(text):
                return int(text) if text.isdigit() else text

            def natural_keys(text):
                return [atoi(c) for c in re.split('(\d+)', text)]

            f.sort(key=natural_keys)

            pdf_bytes = img2pdf.convert(f, dpi=300, x=None, y=None)
            pdf_bfr = BytesIO()
            with open(pdf_file_name, "wb") as doc:
                doc.write(pdf_bytes)

            with open(pdf_file_name, "rb") as fp:
                pdf_bfr.write(fp.read())
            pdf_bfr.write(pdf_bytes)
            pdf_bfr.seek(0)
            os.remove(pdf_file_name)

            return pdf_bfr, pdf_file_name
        except Exception as e:
            print(e)
            return None, None
