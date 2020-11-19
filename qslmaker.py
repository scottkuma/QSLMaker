import adif_io as aio
#import pprint
from PIL import Image, ImageDraw, ImageFont
import os

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    import re
    #value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = str(re.sub('[^\w\s-]', '', value).strip().lower())
    value = str(re.sub('[-\s]+', '-', value))
    # ...
    return value

def drawCenteredText(text, textarea, font_in, font_color='rgb(0,0,0)'):
    #returns a two-tuple (x,y) location for text.
    #note: ONLY CENTERS HORIZONTALLY at this time
    w, h = draw.textsize(text, font=font_in)
    x = ((textarea['size'][0] - w)/2) + textarea['offset'][0]
    y = ((textarea['size'][1] - h)/2) + textarea['offset'][1]

    draw.text((x,y), text, font=font_in, fill=font_color)


fontfile = 'Roboto/Roboto-Regular.ttf'
font = ImageFont.truetype(fontfile, size=72)

boldfontfile = 'Roboto/Roboto-Black.ttf'
bold_font = ImageFont.truetype(boldfontfile, size=72)

freq_font = ImageFont.truetype(fontfile, size=60)

imageinfo = [{'filename': '20081010-DigitalQSL.jpg',
             'fields':{
                 'to_radio': {'offset':(100,754), 'size':(350,108)},
                 'date_d': {'offset':(456, 754), 'size':(116,108)},
                 'date_m': {'offset':(578, 754), 'size':(104,108)},
                 'date_y': {'offset':(689, 754), 'size':(126,108)},
                 'time_on': {'offset':(823,754), 'size':(218,108)},
                 'freq': {'offset':(1046, 754), 'size':(260,108)},
                 'mode': {'offset':(1314, 754), 'size':(214,108)},
                 'rst': {'offset':(1538,754), 'size':(185,108)},
                 'confirm_qso': {'offset':(1141, 495), 'size':(52,52)},
                 'pse_qsl': {'offset':(82, 498), 'size':(52,52)},
                 '73': {'offset':(1196, 895), 'size':(518,107)}
                 }},
             {'filename': '20081010-GenericQSL.jpg',
             'fields':{
                 'to_radio': {'offset':(100,754), 'size':(350,108)},
                 'date_d': {'offset':(456, 754), 'size':(116,108)},
                 'date_m': {'offset':(578, 754), 'size':(104,108)},
                 'date_y': {'offset':(689, 754), 'size':(126,108)},
                 'time_on': {'offset':(823,754), 'size':(218,108)},
                 'freq': {'offset':(1046, 754), 'size':(260,108)},
                 'mode': {'offset':(1314, 754), 'size':(214,108)},
                 'rst': {'offset':(1538,754), 'size':(185,108)},
                 'confirm_qso': {'offset':(1130, 501), 'size':(52,52)},
                 'pse_qsl': {'offset':(90, 498), 'size':(52,52)},
                 '73': {'offset':(1196, 895), 'size':(518,107)}
                 }}
             ]

CARDNO = 1

adif_file = "wsjtx_log_ORIG.adi"

adif = aio.read_from_file(adif_file)

black = 'rgb(0,0,0)'
red = 'rgb(255,0,0)'



for qso in adif[0]:
    print(f"Working on {qso['CALL']}")
    image = Image.open(imageinfo[CARDNO]['filename'])
    fields = imageinfo[CARDNO]['fields']
    #print(fields)
    draw = ImageDraw.Draw(image)
    #Call

    drawCenteredText(qso['CALL'], fields['to_radio'], bold_font, black)

    #QSO date
    day = qso['QSO_DATE'][-2:]
    month = qso['QSO_DATE'][4:6]
    year = qso['QSO_DATE'][2:4]


    drawCenteredText(day, fields['date_d'], bold_font, black)
    drawCenteredText(month, fields['date_m'], bold_font, black)
    drawCenteredText(year, fields['date_y'], bold_font, black)

    #QSO time_on
    time_on = qso['TIME_ON'][:2] + ":" + qso['TIME_ON'][2:4]
    drawCenteredText(time_on, fields['time_on'], bold_font, black)

    #QSO Frequency
    freq = qso['FREQ'][:8]
    drawCenteredText(freq, fields['freq'], freq_font, red)

    #QSO mode
    qso_mode = qso['MODE']
    drawCenteredText(qso_mode, fields['mode'], bold_font, black)

    #RST
    rst = qso['RST_SENT']
    drawCenteredText(rst, fields['rst'], bold_font, black)

    #confirm QSO
    drawCenteredText('x', fields['confirm_qso'], bold_font, red)

    #pse QSL
    #draw.text(imageinfo['pse_qsl'], 'x', fill=red, font=bold_font)
    drawCenteredText('x', fields['pse_qsl'], bold_font, red)

    filecall = slugify(qso['CALL'])
    filedatetime = str(qso['QSO_DATE'][:4])+str(month)+str(day) + '_' + str(qso['TIME_ON'])
    if not os.path.exists('out'):
        os.makedirs('out')
    image.save(f"out/{filecall}_{filedatetime}.jpg")
