# img_viewer.py

import PySimpleGUI as sg
import os.path
import obspy
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from obspy.clients.seedlink import Client 
client = Client('10.246.1.141')

def plot_waveform(mseed):
    mseed.detrend("demean")
    mseed.filter("bandpass", freqmin=2,freqmax=20) 
    mseed.taper(0.05)

    day=mseed[0].stats.starttime.day
    month=mseed[0].stats.starttime.month
    year=mseed[0].stats.starttime.year
    data = str(day)+"-"+str(month)+"-"+str(year)
    
    hour=mseed[0].stats.starttime.hour
    minute=mseed[0].stats.starttime.minute
    second=mseed[0].stats.starttime.second
    ora=str(hour)+":"+str(minute)

    fig = plt.figure(figsize=(15, 7))

    axs = fig.subplots(3, 1, sharex=True, gridspec_kw={'hspace': 0})

    for i in range(3):
        axs[i].set_yticks([])

    axs[0].plot(mseed.select(component="Z")[0].times(), mseed.select(component="Z")[0].data, label='Verticale', color=(0.49,0.8,0.85),lw=2)
    axs[1].plot(mseed.select(component="N")[0].times(), mseed.select(component="N")[0].data, label='N-S' , color=(0.58,0.65,0.28),lw=2)
    axs[2].plot(mseed.select(component="E")[0].times(), mseed.select(component="E")[0].data, label='E-W', color=(0.91,0.17,0.16),lw=2)

    axs[2].set_xlabel("Tempo (secondi)",fontsize=16)
    axs[1].set_ylabel("Velocità (metri al secondo) ",fontsize=16)
    axs[0].set_title("Hai saltato a Lucca Comics il "+data+" alle ore "+ora,fontsize=18)

    axs[0].legend(fontsize=12)
    axs[1].legend(fontsize=12)
    axs[2].legend(fontsize=12)
    plt.tight_layout()
    savefig('earthquake.png')
    return 

# First the window layout in 2 columns

file_list_column = [
    [
        sg.Text("INGV ShakeApp")],
    [    
        sg.Button('START')],
    [
        sg.Button('STOP')
    ],
    [
        sg.Button('SHOW')
    ],

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

window = sg.Window("Image Viewer", layout)

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
        endtime = obspy.UTCDateTime.now()
        print(endtime)
        start=starttime
        end=endtime
        stream = client.get_waveforms("ET",'SOE2','','HH?',start,end)
        plot_waveform(stream)
        # try:
        #     # Get list of files in folder
        #     #file_list = os.listdir(folder)
        # except:
        #     #file_list = []
    elif event == "SHOW":  # A file was chosen from the listbox
        try:
            # start=starttime
            # command = ""
            # cmd = command
            filename = 'earthquake.png'
            #window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)

        except:
            pass

window.close()
