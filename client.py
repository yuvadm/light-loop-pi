from unipath import FSPath as Path

DATA_DIR = Path(__file__).absolute().ancestor(1).child('data')


class LightLoopClient(object):
    def __init__(self):
        self.sequences = {}
        self.compostion = []
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
            name, sequence_data = lines[0].strip(), [map(int, list(x)) for x in filter(lambda x: x != '', lines[1:])]
            self.sequences[name] = sequence_data

    def init_composition(self, composition_data):
        self.composition = [c.split(',') for c in composition_data.split('\n')[1:]]    

    def process_single_loop(self):
        for c in self.composition:
            pass

    def loop(self):
        print self
            

if __name__ == '__main__':
    client = LightLoopClient()
    client.loop()
