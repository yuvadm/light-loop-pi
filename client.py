from unipath import FSPath as Path

DATA_DIR = Path(__file__).absolute().ancestor(1).child('data')

sequences = {}

with open(DATA_DIR.child('data.txt'), 'r') as f:
    data = f.read()
    sequence_data, composition_data = data.split('\n===\n')

    for sequence in sequence_data.split('#')[1:]:
        lines = sequence.split('\n')
        name, sequence_data = lines[0].strip(), filter(lambda x: x != '', lines[1:]).split()
        sequences[name] = sequence_data

    composition = composition_data.split('\n')[1:]

    print composition
    print sequences
