import os



examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../examples')

examples = []



for filename in os.listdir(examples_dir):
    if filename.endswith('.txt'):
        path = os.path.join(examples_dir, filename)
        with open(path, 'rb') as examplefile:
            examplebodies = [body.strip() for body in examplefile.read().split('---')]
            for index, body in enumerate(examplebodies):
                try:
                    high, low, flags, text = body.split('\n', 3)
                    examples.append({
                        'high': high.split(' '),
                        'low': low.split(' '),
                        'flags': flags.split(' '),
                        'text': text,
                        'name': '%s #%d' % (filename, index+1)
                    })
                except:
                    pass
