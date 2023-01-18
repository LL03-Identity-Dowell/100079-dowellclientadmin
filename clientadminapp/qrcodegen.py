import qrcode
from PIL import Image
from cryptography.fernet import Fernet
import json
def encode(key,text):
    cipher_suite = Fernet(key.encode())
    encoded_text = cipher_suite.encrypt(text.encode())
    return encoded_text
def qrgen(img,link,brand,product,outimg,logoname):
    # import modules


    # taking image which user wants
    # in the QR code center
    Logo_link = img

    logo = Image.open(Logo_link)

    # taking base width
    basewidth = 100
    # adjust image size
    wpercent = (basewidth/float(logo.size[0]))
    hsize = int((float(logo.size[1])*float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    # taking url or text
    url = f'{link}?brand={brand}&product={product}&logo={logoname}'

    # adding URL or text to QRcode
    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    QRcolor = 'black'

    # adding color to QR code
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="#DCDCDC").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    # save the QR code generated
    QRimg.save(outimg)
#qrcodegen("r.jpg","https://www.geeksforgeeks.org/","coco","pepsi","myimg.png")
def qrgen1(user,userid,imgout):
    # Data to be encoded
    # Encoding data using make() function
    dic={"username":user,"userid":userid}
    img = qrcode.make(json.dumps(dic))

    # Saving as an image file
    img.save(imgout)