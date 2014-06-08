from itertools import cycle
from pprint import pprint
from time import sleep
from unipath import FSPath as Path

DATA_DIR = Path(__file__).absolute().ancestor(1).child('data')


class LightLoopClient(object):
    def __init__(self):
        self.sequences = {}
        self.composition = []
        self.tempo = 0.3
        self.init_serial()
        self.init_data()
        self.prepare_data()

    def __str__(self):
        return '{}\n{}\n{}'.format(self.sequences, self.composition, self.tempo)

    def init_serial(self):
        self.serial = open(DATA_DIR.child('serial.out'), 'a')

    def init_data(self):
        with open(DATA_DIR.child('data.txt'), 'r') as f:
            sequence_data, composition_data = f.read().split('\n===\n')
            self.init_sequences(sequence_data)
            self.init_composition(composition_data)

    def init_sequences(self, sequence_data):
        for sequence in sequence_data.split('#')[1:]:
            lines = sequence.split('\n')
            name, sequence_data = lines[0].strip(), [list(x) for x in filter(lambda x: x != '', lines[1:])]
            self.sequences[name] = sequence_data

    def init_composition(self, composition_data):
        composition_data = filter(lambda x: x != '', composition_data.split('\n'))
        self.tempo = float(composition_data[0].split('_')[1]) / 1000.0
        self.composition = [c.split(',') for c in composition_data[1:]]

    def gen_packet(self, tree, channel, mode):
        if tree > 7 or channel > 7 or mode > 1:
            raise Exception('Bad values')
        return chr((tree << 5) | (channel << 2) | mode)

    def prepare_data(self):
        data = []
        for frame in zip(*self.composition):
            sequences = [zip(*self.sequences[seq]) for seq in frame]
            sequences = zip(*sequences)
            # print ''.join([''.join([''.join(y) for y in x]) for x in sequences])
            data.append(sequences)

        self.data_packets = []
        for sequence in data:
            for frame in sequence:
                frame_packets = bytearray()
                for tree, tree_frame in enumerate(frame):
                    for channel, mode in enumerate(tree_frame):
                        tree, channel, mode = map(int, [tree, channel, mode])
                        # print 'tree {} channel {} mode {}'.format(tree, channel, mode)
                        packet = self.gen_packet(tree, channel, mode)
                        frame_packets.append(packet)
                self.data_packets.append(frame_packets)
                # print 'sleep'

    def write(self, packets):
        self.serial.write(packets)
        self.serial.flush()

    def loop(self):
        for frame in cycle(self.data_packets):
            self.write(frame)
            sleep(self.tempo)
            

if __name__ == '__main__':
    client = LightLoopClient()
    client.loop()
