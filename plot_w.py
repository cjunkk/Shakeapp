def plot_waveform(mseed):
    import datetime
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import savefig
    import matplotlib.image as mpimg
    mseed.detrend("demean")
    mseed.filter("bandpass", freqmin=2,freqmax=20) 
    mseed.taper(0.05)

    utc=mseed[0].stats.starttime+3600
    dt = datetime.datetime.strptime(str(utc), "%Y-%m-%dT%H:%M:%S.%fZ")
    #print(dt.strftime("%H"),dt.strftime("%M"))

    day=dt.strftime("%d")
    month=dt.strftime("%m")
    year=dt.strftime("%Y")
    data = str(day)+"-"+str(month)+"-"+str(year)
    
    hour=dt.strftime("%H")
    minute=dt.strftime("%M")
    second=dt.strftime("%S")
    ora=str(hour)+":"+str(minute)+":"+str(second)

    fig = plt.figure(figsize=(26, 14))
    axs = fig.subplots(3, 1, sharex=True, gridspec_kw={'hspace': 0})

    for i in range(3):
        axs[i].set_yticks([])

    axs[0].plot(mseed.select(component="Z")[0].times(), mseed.select(component="Z")[0].data, label='Verticale', color=(0.49,0.8,0.85),lw=2)
    axs[1].plot(mseed.select(component="N")[0].times(), mseed.select(component="N")[0].data, label='N-S' , color=(0.58,0.65,0.28),lw=2)
    axs[2].plot(mseed.select(component="E")[0].times(), mseed.select(component="E")[0].data, label='E-W', color=(0.91,0.17,0.16),lw=2)

    axs[2].set_xlabel("Tempo (secondi)",fontsize=36)
    axs[1].set_ylabel("Velocità del suolo ",fontsize=36)
    axs[0].set_title("Hai saltato a Lucca Comics il "+data+" alle ore "+ora,fontsize=48)

    axs[0].legend(fontsize=24)
    axs[1].legend(fontsize=24)
    axs[2].legend(fontsize=24)
    plt.xticks(fontsize=24)
    plt.tight_layout()
    savefig('earthquake.png',dpi=300)
    plt.close()
    return
def mosaic():
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import savefig
    import matplotlib.image as mpimg
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
    plt.savefig('mosaic.png')
    plt.close()
    return