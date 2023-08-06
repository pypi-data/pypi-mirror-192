# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jamexp', 'jamexp.cli', 'jamexp.hyd', 'jamexp.utils', 'jamexp.wandb_clean']

package_data = \
{'': ['*'], 'jamexp': ['template_data/*']}

install_requires = \
['GitPython>=3.1.17,<4.0.0',
 'Pillow>=8.2.0,<9.0.0',
 'gpustat>=0.6.0,<0.7.0',
 'hydra-core>=1.0.6,<2.0.0',
 'loguru>=0.5.3,<0.6.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pyfzf>=0.2.2,<0.3.0',
 'pylint>=2.8.3,<3.0.0',
 'scipy>=1.6.3,<2.0.0',
 'typer>=0.3.2,<0.4.0',
 'wandb>=0.10.30,<0.11.0']

entry_points = \
{'console_scripts': ['jcpt = jamexp.cli.jcp_template:cp_template',
                     'jhelp = jamexp.cli.helper:run_helper',
                     'jhydc = jamexp.cli.jhyd_clean:main',
                     'jkill = jamexp.cli.jckill:cudakillfzf',
                     'jkilla = jamexp.cli.jckill:cudakill',
                     'jln = jamexp.cli.jlink:link',
                     'jnb_clean = jamexp.cli.jnb_clean:main',
                     'jpin = jamexp.cli.jpin:main',
                     'jstar = jamexp.cli.star_file:main',
                     'junln = jamexp.cli.jlink:unlink',
                     'jwb_check_running = jamexp.cli.jwb_check_running:main',
                     'jwdc = jamexp.cli.jwb_clean:main',
                     'ngc_bash = jamexp.cli.ngc_shell:ngc_bash',
                     'ngc_kill = jamexp.cli.ngc_shell:ngc_kill',
                     'ngc_list = jamexp.cli.ngc_shell:ngc_list',
                     'ngc_result = jamexp.cli.ngc_shell:ngc_result']}

setup_kwargs = {
    'name': 'jamexp',
    'version': '0.1.6',
    'description': 'Jam Experiment helper',
    'long_description': '# jamexp\n\n## cli\n\n* `jstar`: star files with fzf prompt.\n\n### `jwdc`: clear stale, short and notag\n```shell\nexport WANDB_ENTITY=name\nexport WANDB_API_KEY=key\n```\n\n* `stale`: [0, 10], [7, 60], [3, 180], [1, 600] (days, run_duration/seconds)\n* `short`: three days ago and no tags\n\n### `jhydc`: clear hyd exp folders\n\n* `stale`: [0, 10], [7, 60], [3, 180], [1, 600]\n* `wandb-sync`\n\n* `jpin`: pin good results\n\n### `jln` and `junln`\n',
    'author': 'Qinsheng',
    'author_email': 'qsh.zh27@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
