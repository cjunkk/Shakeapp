import PySimpleGUI as sg
sg.set_options(font=('Arial Bold', 16))
import os.path
import obspy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import requests
import datetime
import base64
import qrcode
import io
from PIL import Image
from matplotlib.pyplot import savefig
from obspy.clients.seedlink import Client
from plot_w import mosaic
# set Seedlink server
client = Client('discovery.ingv.it',port=39962)
client = Client('rs-2.local')
# Set API endpoint and headers
url = "https://api.imgur.com/3/image"
headers = {"Authorization": "Client-ID bd1de98fb9a0d89"}

def plot_waveform(mseed):
    mseed.detrend("demean")
    mseed.filter("bandpass", freqmin=2,freqmax=20) 
    mseed.taper(0.05)

    utc=mseed[0].stats.starttime
    dt = datetime.datetime.strptime(str(utc), "%Y-%m-%dT%H:%M:%S.%fZ")
    print(dt.strftime("%H"),dt.strftime("%M"))

    day=dt.strftime("%d")
    month=dt.strftime("%m")
    year=dt.strftime("%Y")
    data = str(day)+"-"+str(month)+"-"+str(year)
    
    hour=dt.strftime("%H")
    minute=dt.strftime("%M")
    second=dt.strftime("%S")
    ora=str(hour)+":"+str(minute)+":"+str(second)
    
    fig = plt.figure(figsize=(15, 7))

    axs = fig.subplots(3, 1, sharex=True, gridspec_kw={'hspace': 0})

    for i in range(3):
        axs[i].set_yticks([])

    axs[0].plot(mseed.select(component="Z")[0].times(), mseed.select(component="Z")[0].data, label='Verticale', color=(0.49,0.8,0.85),lw=2)
    axs[1].plot(mseed.select(component="N")[0].times(), mseed.select(component="N")[0].data, label='N-S' , color=(0.58,0.65,0.28),lw=2)
    axs[2].plot(mseed.select(component="E")[0].times(), mseed.select(component="E")[0].data, label='E-W', color=(0.91,0.17,0.16),lw=2)

    axs[2].set_xlabel("Tempo (secondi)",fontsize=16)
    axs[1].set_ylabel("Velocità del suolo ",fontsize=16)
    axs[0].set_title("Hai saltato a Lucca Comics il "+data+" alle ore "+ora,fontsize=18)

    axs[0].legend(fontsize=12)
    axs[1].legend(fontsize=12)
    axs[2].legend(fontsize=12)
    plt.tight_layout()
    savefig('earthquake.png')
    return 

def mosaic():
    fig, axd = plt.subplot_mosaic(
    [["lucca"],
     ['linea'],
     ["mseed"],
     ['ingv']
    ],
    layout="constrained",
    # "image" will contain a square image. We fine-tune the width so that
    # there is no excess horizontal or vertical margin around the image.
    height_ratios=[1.3,.5,4.5,.35],
    width_ratios=[1],
    )
    #fig = plt.figure(dpi=300, tight_layout=True)
    fig.set_size_inches(11.69, 8.27, forward=True)
    fig.set_size_inches(11.69, 8.27, forward=True)
    # Plot the MRI image
    im=mpimg.imread('./logo-lcg-edizione-2023.png')
    axd["lucca"].imshow(im)
    axd["lucca"].axis('off')
    im=mpimg.imread('./linea.png')
    axd["linea"].imshow(im)
    axd["linea"].axis('off')
    im=mpimg.imread('./INGV_LOGO_STESO.png')
    axd["ingv"].imshow(im)
    axd["ingv"].axis('off')
    im=mpimg.imread('./earthquake.png')
    axd["mseed"].imshow(im)
    axd["mseed"].axis('off')
    plt.tight_layout()
    #plt.show()
    savefig('mosaic.png')
    img = Image.open('mosaic.png')
    width, height = img.size
    smig = img.resize((width//2,height//2))
    smig.save('smosaic.png','PNG')
    # plt.close()
    return

# First the window layout in 2 columns
file_list_column = [
    #[sg.Text(text = "INGV ShakeApp", size=20, justification='center',expand_x=True)],
    [sg.Image('INGV.png')],
    [sg.HSeparator()],
    [sg.Button('START'),
    sg.Button('STOP'),
    sg.Button('SHOW'),
    sg.Button("PRINT"),
    sg.Button("QRCODE")]
    ]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Ecco il tuo salto")],
    #[sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("INGV Shaking Viewer", layout,resizable=True)

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "START":
        starttime = obspy.UTCDateTime.now()
        print(starttime)
        # try:
        #     # Get list of files in folder
        #     #file_list = os.listdir(folder)
        # except:
        #     #file_list = []
    if event == "STOP":
        time.sleep(10)
        endtime = obspy.UTCDateTime.now()
        print(endtime)
        start=starttime
        end=endtime
        stream = client.get_waveforms("AM",'R08EF','00','EH?',start,end)
        plot_waveform(stream)
        mosaic()
        # try:
        #     # Get list of files in folder
        #     #file_list = os.listdir(folder)
        # except:
        #     #file_list = []
    if event == "QRCODE":  # A file was chosen from the listbox
        try:
            with open("mosaic.png", "rb") as file:
                data = file.read()
                base64_data = base64.b64encode(data)
                # Upload image to Imgur and get URL
                response = requests.post(url, headers=headers, data={"image": base64_data})
                url = response.json()["data"]["link"]
                print(url)
                qr = qrcode.QRCode(version=3, box_size=10, border=5, error_correction=qrcode.constants.ERROR_CORRECT_H)
                # Define the data to be encoded in the QR code
                data = url
                # Add the data to the QR code object
                qr.add_data(data)
                # Make the QR code
                qr.make(fit=True)
                # Create an image from the QR code with a black fill color and white background
                img = qr.make_image(fill_color="black", back_color="white")
                # Save the QR code image
                img.save("qr_code.png")
            # start=starttime
            # command = ""
            # cmd = command
            filename = 'qr_code.png'
            #window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)
        except:
            pass
    if event == "SHOW":  # A file was chosen from the listbox
        try:
            # start=starttime
            # command = ""
            # cmd = command
            filename = 'smosaic.png'
            #window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)

        except:
            pass
    if event == "PRINT":  # print image
        try:
            os.system('lp mosaic.png')
        except:
            pass

window.close()
