from matplotlib import pyplot as plt

channel_colors = {'Traps': '#FA0909',
                  'Addressability': '#F00E0E',
                  'Imaging': '#000000',
                  'Optical pumping': '#F00E0E',
                  'Repumper': '#FA0909',
                  'Push-out': '#000000',
                  '1013': '#880808',
                  '420': '#0F9FE3',
}

class Channel():
    def __init__(self, name=''):
        self.name = name
        self.color = [0, 0, 0]
        self.values = None
        self.timings = []
        self.ramp = None

class Sequence():
    def __init__(self, name=''):
        self.name = name
        self.channels = []
        self.n_channels = 0
        self.max_time = 0
        self.min_time = 0

    def add_channel(self, channel):
        self.channels.append(channel)
        self.n_channels += 1

    def get_max_time(self):
        for channel in self.channels:
            t = channel.timings[-1]
            if t > self.max_time:
                self.max_time = t

    def get_min_time(self):
        for channel in self.channels:
            t = channel.timings[0]
            if t < self.min_time:
                self.min_time = t

    def draw(self):
        self.get_max_time()
        self.get_min_time()
        fig = plt.figure(figsize=(6, self.n_channels*1.2))
        fig.canvas.manager.set_window_title(self.name)
        fig.suptitle(self.name)
        gs = fig.add_gridspec(self.n_channels, hspace=0)
        ha = gs.subplots(sharex=True, sharey=False)
        for i, channel in enumerate(self.channels):
            graph_data_x = []
            graph_data_y = []
            if channel.ramp:
                for j in range(len(channel.timings)-1):
                    graph_data_x.append(channel.timings[j])
                    graph_data_x.append(channel.timings[j+1])
                    if type(channel.values) is list:
                        value = channel.values[j]
                    else:
                        value = channel.values%2
                        channel.values += 1
                    graph_data_y.append(value)
                    if type(channel.values) is list:
                        value = channel.values[j+1]
                    else:
                        value = channel.values % 2
                    graph_data_y.append(value)
            else:
                for j in range(len(channel.timings)-1):
                    graph_data_x.append(channel.timings[j])
                    graph_data_x.append(channel.timings[j+1])
                    if type(channel.values) is list:
                        value = channel.values[j]
                    else:
                        value = channel.values%2
                        channel.values += 1
                    graph_data_y.append(value)
                    graph_data_y.append(value)

                    value += 1
            try:
                ax = ha[i]
            except TypeError:
                ax = ha
            if type(channel.values) is list:
                ax.grid()
            else:
                ax.set_ylim([-0.2, 1.2])
            ax.plot(graph_data_x, graph_data_y, color=channel.color)
            ax.set_ylabel(channel.name, rotation=0, weight='bold', labelpad=20)
            ax.set_xlabel('time [ns]')
            if type(channel.values) is list:
                pass
            else:
                plt.sca(ax)
                plt.yticks([0, 1], ['off', 'on'])
        plt.xlim(self.min_time, self.max_time)

        plt.tight_layout()
        plt.show()

def Test():
    MOT = Channel('MOT')
    MOT.color = '#FF3333'
    MOT.values = 1
    MOT.timings = [0, 10, 200]

    OptPump = Channel('Optical\npumping')
    OptPump.color = '#FF3333'
    OptPump.values = 0
    OptPump.timings = [0, 10, 20, 50, 100, 200]

    OptPumpRamp = Channel('feOptical\npumping\nramp')
    OptPumpRamp.color = '#FF3333'
    OptPumpRamp.values = [0, 2.1, 0, 1, 1, 0.2, 0.2, 0]
    OptPumpRamp.timings = [0, 10, 22, 50, 100, 110, 120, 130, 200]

    OptPumpRamp2 = Channel('feOptical\npumping\nramp')
    OptPumpRamp2.color = '#FF3333'
    OptPumpRamp2.values = [0, 0, 2.1, 2.1, 0, 0, 1, 0.2, 0.2, 0, 0]
    OptPumpRamp2.timings = [0, 8, 10, 22, 30, 50, 100, 110, 120, 130, 200]
    OptPumpRamp2.ramp = True

    channels = [MOT, OptPump, OptPumpRamp, OptPumpRamp2]
    sequence = Sequence('SPAM errors - False positive')
    for channel in channels:
        sequence.add_channel(channel)
    sequence.draw()

def ReleaseRecapture():
    channels = []

    channel = Channel('Traps')
    channel.color = '#FF3333'
    channel.values = [10, 10, 5, 5, 0, 0, 5, 5, 10, 10]
    channel.timings = [0, 40, 50, 60, 60, 65, 65, 75, 85, 150]
    channel.ramp = True
    channels.append(channel)

    channel = Channel('Imaging')
    channel.color = '#FF3333'
    channel.values = 0
    channel.timings = [0, 10, 30, 100, 120, 150]
    channel.ramp = False
    channels.append(channel)

    sequence = Sequence('Release - Recapture')
    for channel in channels:
        sequence.add_channel(channel)
    sequence.draw()

def Spectroscopy():
    channels = []

    channel = Channel('Imaging')
    channel.color = channel_colors['Imaging']
    channel.values = 1
    channel.timings = [0, 50, 600, 650]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    channels.append(channel)

    channel = Channel('Traps')
    channel.color = channel_colors['Traps']
    channel.values = [10, 10, 0, 0, 10, 10]
    channel.timings = [0, 100, 200, 700, 800, 900]
    channel.ramp = True
    channel.values = 1
    channel.timings = [0, 100, 550, 650]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    channels.append(channel)

    channel = Channel('1013 nm')
    channel.color = channel_colors['1013']
    channel.values = [0, 0, 30, 30, 0, 0]
    channel.timings = [0, 250, 350, 550, 650, 900]
    channel.ramp = True
    channel.values = 0
    channel.timings = [0, 150, 500, 650]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    channels.append(channel)

    channel = Channel('420 nm')
    channel.color = channel_colors['420']
    channel.values = 0
    channel.timings = [0, 200, 450, 650]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    channels.append(channel)

    sequence = Sequence('Spectroscopy')
    for channel in channels:
        sequence.add_channel(channel)
    sequence.draw()

def Rabi():
    channels = []

    channel = Channel('Imaging')
    channel.color = channel_colors['Imaging']
    channel.values = 1
    channel.timings = [0, 50, 850, 900]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    channels.append(channel)

    channel = Channel('Traps')
    channel.color = channel_colors['Traps']
    channel.values = 1
    channel.timings = [0, 100, 800, 900]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    channels.append(channel)

    channel = Channel('1013 nm')
    channel.color = channel_colors['1013']
    channel.values = 0
    channel.timings = [0, 150, 750, 900]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    channels.append(channel)

    channel = Channel('420 nm')
    channel.color = channel_colors['420']
    channel.values = 0
    channel.timings = [0, 200, 700, 900]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    channels.append(channel)

    sequence = Sequence('Rabi')
    for channel in channels:
        sequence.add_channel(channel)
    sequence.draw()

def Ramsey():
    sequence = Sequence('Ramsey')

    channel = Channel('Imaging')
    channel.color = channel_colors['Imaging']
    channel.values = 1
    channel.timings = [0, 50, 850, 900]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    sequence.add_channel(channel)

    channel = Channel('Traps')
    channel.color = channel_colors['Traps']
    channel.values = 1
    channel.timings = [0, 100, 800, 900]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    sequence.add_channel(channel)

    channel = Channel('1013 nm')
    channel.color = channel_colors['1013']
    channel.values = 0
    channel.timings = [0, 150, 750, 900]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    sequence.add_channel(channel)

    channel = Channel('420 nm')
    channel.color = channel_colors['420']
    channel.values = 0
    channel.timings = [0, 200, 325, 575, 700, 900]
    channel.timings = [x-200 for x in channel.timings]
    channel.ramp = False
    sequence.add_channel(channel)

    sequence.draw()

def OpticalPumping():
    sequence = Sequence('Optical pumping')

    channel = Channel('Repumper')
    channel.color = channel_colors['Repumper']
    channel.values = 1
    channel.timings = [-100, -50, 550, 600]
    channel.ramp = False
    channel.values = [1,1,0,0,0,1,1]
    channel.timings = [-100, -80, -50, -50, 550, 580, 600]
    channel.ramp = True
    sequence.add_channel(channel)

    channel = Channel('Optical\npumping')
    channel.color = channel_colors['Optical pumping']
    channel.values = 0
    channel.timings = [-100, 0, 500, 600]
    channel.ramp = False
    sequence.add_channel(channel)

    channel = Channel('Push-out')
    channel.color = channel_colors['Push-out']
    channel.values = 0
    channel.timings = [-100, 0, 125, 375, 500, 600]
    channel.ramp = False
    sequence.add_channel(channel)

    sequence.draw()

def Addressability():
    sequence = Sequence('Addressability')

    channel = Channel('Traps')
    channel.color = channel_colors['Traps']
    channel.values = 1
    channel.timings = [-100, -50, 550, 600]
    channel.ramp = False
    sequence.add_channel(channel)

    channel = Channel('Add')
    channel.color = channel_colors['Addressability']
    channel.values = 0
    channel.timings = [-100, 0, 500, 600]
    channel.ramp = False
    sequence.add_channel(channel)

    channel = Channel('Push-out')
    channel.color = channel_colors['Push-out']
    channel.values = 0
    channel.timings = [-100, 0, 500, 600]
    channel.ramp = False
    sequence.add_channel(channel)

    sequence.draw()

def main():
    #Test()
    #ReleaseRecapture()
    Spectroscopy()
    Rabi()
    Ramsey()
    # OpticalPumping()
    # Addressability()

if __name__ == "__main__":
    main()