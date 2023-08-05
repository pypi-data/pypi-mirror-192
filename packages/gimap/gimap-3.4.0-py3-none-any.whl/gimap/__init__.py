import os

from .__version__ import __version__


def _get_file(file):
    folder = os.path.dirname(__file__)
    file = os.path.join(folder, file)
    return os.path.abspath(file).replace('\\', '/')

def GIMAP():
    return _get_file('GIMAP_luma_05x_ps.png')


def ARROW():
    return _get_file('ARROW.png')
