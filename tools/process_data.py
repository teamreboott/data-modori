from loguru import logger
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))

sys.path.append(parent_directory)

from data_modori.config import init_configs
from data_modori.core import Executor

@logger.catch
def main():
    cfg = init_configs()
    if cfg.executor_type == 'default':
        executor = Executor(cfg)
    elif cfg.executor_type == 'ray':
        from data_modori.core.ray_executor import RayExecutor
        executor = RayExecutor(cfg)
    executor.run()


if __name__ == '__main__':
    main()
