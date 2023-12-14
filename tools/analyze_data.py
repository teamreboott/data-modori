from loguru import logger

from data_modori.core import Analyser


@logger.catch
def main():
    analyser = Analyser()
    analyser.run()


if __name__ == '__main__':
    main()
