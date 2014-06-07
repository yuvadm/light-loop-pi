from pprint import pprint
from unipath import FSPath as Path

DATA_DIR = Path(__file__).absolute().ancestor(1).child('data')


class LightLoopClient(object):
    def __init__(self):
        self.sequences = {}
        self.composition = []
        self.tempo = 300
        self.init_data()

    def __str__(self):
        return '{}\n{}\n{}'.format(self.sequences, self.composition, self.tempo)

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
        self.tempo = composition_data[0].split('_')[1]
        self.composition = [c.split(',') for c in composition_data[1:]]

    def gen_packet(tree, channel, mode):
        if tree > 7 or channel > 7 or mode > 1:
            raise Exception('Bad values')
        return (tree << 5) | (channel << 2) | mode

    def process_single_loop(self):
        raw_data = ''
        for frame in zip(*self.composition):
            print frame
            sequences = zip(*[zip(*self.sequences[seq]) for seq in frame])
            raw_data += ''.join([''.join([''.join(y) for y in x]) for x in sequences])
        print raw_data

    def loop(self):
        print self
        self.process_single_loop()
            

if __name__ == '__main__':
    client = LightLoopClient()
    client.loop()
