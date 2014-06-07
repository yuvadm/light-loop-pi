from unipath import FSPath as Path

DATA_DIR = Path(__file__).absolute().ancestor(1).child('data')


class LightLoopClient(object):
    def __init__(self):
        self.sequences = {}
        self.compostion = []
        self.init_data()

    def init_data(self):
        with open(DATA_DIR.child('data.txt'), 'r') as f:
            data = f.read()
            sequence_data, composition_data = data.split('\n===\n')

            for sequence in sequence_data.split('#')[1:]:
                lines = sequence.split('\n')
                name, sequence_data = lines[0].strip(), filter(lambda x: x != '', lines[1:])
                self.sequences[name] = sequence_data

            self.composition = composition_data.split('\n')[1:]

    def print_data(self):
        print self.sequences
        print self.composition

    def loop(self):
        self.print_data()
            

if __name__ == '__main__':
    client = LightLoopClient()
    client.loop()
