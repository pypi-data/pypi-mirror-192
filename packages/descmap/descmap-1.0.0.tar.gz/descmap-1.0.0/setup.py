# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['descmap', 'descmap.analysis']

package_data = \
{'': ['*']}

install_requires = \
['chart-studio>=1.1.0',
 'matplotlib>=3.6.3',
 'numpy>=1.24.2',
 'pandas>=1.5.3',
 'pgradd>=2.9.5',
 'plotly>=5.13.0',
 'pmutt>=1.3.2',
 'pydoe>=0.3.8',
 'rdkit>=2022.9.4',
 'scikit-learn>=1.2.1',
 'scipy>=1.10.0',
 'vunits>=0.0.4',
 'xlsxwriter>=3.0.8']

setup_kwargs = {
    'name': 'descmap',
    'version': '1.0.0',
    'description': 'Automatic feature selection and volcano curve generation.',
    'long_description': "Descriptor-Based Microkinetic Analyais Package (DescMAP)\n========================================================\n\nThe **Desc**\\ riptor-Based **M**\\ icrokinetic **A**\\ nalysis\n**P**\\ ackage (DescMAP) is a Python library developed by the Vlachos\nResearch Group at the University of Delaware. This code was developed to\nautomate descriptor selection and volcano curve generation for\nheterogeneous catalysis using empirical and semi-empirical approaches\ncoupled with microkinetic modeling. Both electronic and geometric\ndescriptors are supported. Inputting data via spreadsheets and\ncontrolling program behavior via template files increases flexibility\nand supported capabilities.\n\n.. image:: https://raw.githubusercontent.com/VlachosGroup/DescriptorMap/master/docs/logos/descmap_logo.png\n    :width: 400px\n\nDocumentation\n-------------\n\nSee our `documentation page <https://descriptormap.readthedocs.io/en/latest/>`__ for \ndocstrings and more details.\n\n\nGetting Started\n---------------\n\n1. Install using pip (see documentation for full instructions)\n\n.. code:: bash\n\n   $ pip install descmap\n\n2. Look at the provided examples\n\n\nDevelopers\n----------\n\n-  Jonathan Lym (jonathanlym@gmail.com)\n-  Xue Zong (xzong@udel.edu)\n\n\nDependencies\n------------\n\n-  Python >= 3.9\n-  `Numpy <http://www.numpy.org/>`__: Used for vector and matrix operations\n-  `Pandas <https://pandas.pydata.org/>`__: Used to import data from Excel or CSV files\n-  `Scipy <https://www.scipy.org/>`__: Used for curve fitting\n-  `Scikit-Learn <https://scikit-learn.org/stable/>`__: Choose\n   descriptors based on DFT data\n-  `RDKit <https://www.rdkit.org/docs/Overview.html>`__: Used for \n   constructing feasible chemical structures required by pGradd\n-  `Matplotlib <https://matplotlib.org/>`__: Used for generating plots\n-  `Plotly <https://plotly.com/>`__: Plots interactive volcano curves\n-  `Chart-studio <https://chart-studio.plotly.com/feed/#/>`__: Provide utilities \n   for interfacing with Plotly's Chart Studio service\n-  `pMuTT <https://vlachosgroup.github.io/pMuTT/>`__: Generates input files for OpenMKM\n-  `pGradd <https://github.com/VlachosGroup/PythonGroupAdditivity/>`__: Estimate \n   thermodynamic properties of molecules\n-  `VUnits <https://vlachosgroup.github.io/vunits/>`__: Unit conversion and constants\n-  `xlsxwriter <https://xlsxwriter.readthedocs.io/>`__: Create Excel xlsx files\n-  `pyDOE <https://pythonhosted.org/pyDOE/>`__: Experimental design package to \n   provide sampling method\n\n\nLicense\n-------\n\nThis project is licensed under the MIT License - see the LICENSE.md file\nfor details.\n\n\nContributing\n------------\n\nIf you have any suggestion or find a bug, please post to our Issues page\non GitHub.\n\n\nQuestions\n---------\n\nIf you have any question or run into any issue, please post to our\nIssues page on GitHub.\n\n\nFunding\n-------\n\nThis material is based upon work supported by the Department of Energy's\nOffice of Energy Efficient and Renewable Energy's Advanced Manufacturing\nOffice under Award Number DE-EE0007888-9.5.\n",
    'author': 'Xue Zong',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
