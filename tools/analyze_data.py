from loguru import logger
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))

sys.path.append(parent_directory)

from data_modori.core import Analyser

@logger.catch
def main():
    analyser = Analyser()
    analyser.run()


if __name__ == '__main__':
    main()
