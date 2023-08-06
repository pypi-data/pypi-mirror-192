import sys

from .hdf5_viewer import EDITOR, APP


if __name__ == "__main__":
    if len(sys.argv) > 1:
        FILE_PATH = sys.argv[1]
        EDITOR.open_file(FILE_PATH)
    APP.exec()
