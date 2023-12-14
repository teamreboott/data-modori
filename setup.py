import logging
import os.path
import re

import setuptools


def get_package_dir():
    pkg_dir = {
        'data_modori.tools': 'tools',
    }
    return pkg_dir


def get_install_requirements(require_f_paths, env_dir='environments'):
    reqs = []
    for path in require_f_paths:
        target_f = os.path.join(env_dir, path)
        if not os.path.exists(target_f):
            logging.warning(f'target file does not exist: {target_f}')
        else:
            with open(target_f, 'r', encoding='utf-8') as fin:
                reqs += [x.strip() for x in fin.read().splitlines()]
    reqs = [x for x in reqs if not x.startswith('#')]
    return reqs


# allowing selective installment based on users' needs
# TODO: The specific taxonomy and dependencies will be determined
#  after implementing some preliminary operators and detailed discussions
# min_requires = get_install_requirements(['minimal_requires.txt'])
# extra_requires = {
#     'mini':
#     min_requires,
#     'sci':
#     get_install_requirements(['science_requires.txt']),
#     'dist':
#     get_install_requirements(['dist_requires.txt']),
#     'dev':
#     get_install_requirements(['dev_requires.txt']),
#     'tools':
#     get_install_requirements(
#         ['preprocess_requires.txt', 'quality_classifier_requires.txt']),
# }
# extra_requires['all'] = [v for v in extra_requires.values()]

require_list = get_install_requirements(['requirements.txt'])

with open('data_modori/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(),
                        re.MULTILINE).group(1)

with open('README.md', encoding='utf-8') as f:
    readme_md = f.read()

setuptools.setup(
    name='data-modori',
    version=version,
    url='https://github.com/teamreboott/data-modori',
    author='TeamAR of Teamreboott',
    description='LMOps Tool for Korean',
    long_description=readme_md,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    packages=setuptools.find_packages(exclude=['tools*'])
            + list(get_package_dir().keys()),
    package_dir=get_package_dir(),
    entry_points={
        'console_scripts': [
            'dm-process = data_modori.tools.process_data:main',
            'dm-analyze = data_modori.tools.analyze_data:main',
        ]
    },
    install_requires=require_list,
    # extras_require=extra_requires,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
)