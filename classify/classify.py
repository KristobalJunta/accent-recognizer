from pybrain2.tools.customxml.networkreader import NetworkReader
from scikits.talkbox.features import mfcc
import numpy as np
import scipy.io.wavfile
import sys
from glob import glob


def classify(file_name):
    accents = [
        "CH",
        "EN",
        "IN",
        "IR",
        "IT",
        "JA",
        "KO",
    ]

    models = glob("models/model*.xml")
    models.sort()
    if len(models) < 1:
        print "no models found"
        exit()

    print "using model: {}".format(models[-1])

    net = NetworkReader.readFrom(models[-1])

    sample_rate, X = scipy.io.wavfile.read(file_name)
    ceps, mspec, spec = mfcc(X)

    x = []
    num_ceps = len(ceps)
    x.append(np.mean(ceps[int(num_ceps / 10):int(num_ceps * 9 / 10)], axis=0))
    vx = np.array(x)

    result = net.activate(vx[0].tolist()).tolist()
    # print result

    accent = accents[result.index(max(result))]
    return accent


if __name__ == 'main':
    filename = sys.argv[1]
    if not filename or type(filename) != str:
        filename = input('Provide a path to audio file: ')
    res = classify(filename)
    print(res)
