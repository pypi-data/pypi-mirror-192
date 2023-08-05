# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minineedle']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'minineedle',
    'version': '3.0.2',
    'description': 'Needleman-Wunsch and Smith-Waterman algorithms in python for any iterable objects.',
    'long_description': '![Build Status](https://github.com/scastlara/minineedle/actions/workflows/python-app.yml/badge.svg) [![PyPI version](https://badge.fury.io/py/minineedle.svg)](https://badge.fury.io/py/minineedle)\n\n<img width="250" src="https://github.com/scastlara/minineedle/blob/master/assets/logo.png"/>\n\nNeedleman-Wunsch and Smith-Waterman algorithms in python for any iterable objects.\n\n## Algorithms\n\n### Needleman-Wunsch\n<img src="https://upload.wikimedia.org/wikipedia/commons/3/3f/Needleman-Wunsch_pairwise_sequence_alignment.png" width="300px">\n\n> The Needleman–Wunsch algorithm is an algorithm used in bioinformatics to align protein or nucleotide sequences. It was one of the first applications of dynamic programming to compare biological sequences. The algorithm was developed by Saul B. Needleman and Christian D. Wunsch and published in 1970. The algorithm essentially divides a large problem (e.g. the full sequence) into a series of smaller problems and uses the solutions to the smaller problems to reconstruct a solution to the larger problem. It is also sometimes referred to as the optimal matching algorithm and the global alignment technique. The Needleman–Wunsch algorithm is still widely used for optimal global alignment, particularly when the quality of the global alignment is of the utmost importance. \n>\n> -- From the <cite>[Wikipedia article](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm)</cite>\n\n### Smith-Waterman\n<img src="https://upload.wikimedia.org/wikipedia/commons/9/92/Smith-Waterman-Algorithm-Example-En.gif" width="300px">\n\n> The Smith–Waterman algorithm performs local sequence alignment; that is, for determining similar regions between two strings of nucleic acid sequences or protein sequences. Instead of looking at the entire sequence, the Smith–Waterman algorithm compares segments of all possible lengths and optimizes the similarity measure. \n>\n> -- From the <cite>[Wikipedia article](https://en.wikipedia.org/wiki/Smith–Waterman_algorithm)</cite>\n\n\n## Usage\n\n```python\nfrom minineedle import needle, smith, core\n\n# Use miniseq objects\n# Load sequences as miniseq FASTA object\nimport miniseq\nfasta = miniseq.FASTA(filename="myfasta.fa")\nseq1, seq2 = fasta[0], fasta[1]\n\n# Or use strings, lists, etc\n# seq1, seq2 = "ACTG", "ATCTG"\n# seq1, seq2 = ["A","C","T","G"], ["A","T","C","T","G"]\n\n# Create the instance\nalignment = needle.NeedlemanWunsch(seq1, seq2)\n# or\n# alignment = smith.SmithWaterman(seq1, seq2)\n\n# Make the alignment\nalignment.align()\n\n# Get the score\nalignment.get_score()\n\n# Get the sequences aligned as lists\nal1, al2 = alignment.get_aligned_sequences("list")\n\n# Get the sequences as strings\nal1, al2 = alignment.get_aligned_sequences("str")\n\n# Change the matrix and run again\nalignment.change_matrix(core.ScoreMatrix(match=4, miss=-4, gap=-2))\nalignment.align()\n\n# Print the sequences aligned\nprint(alignment)\n\n# Change gap character\nalignment.gap_character = "-gap-"\nprint(alignment)\n\n# Sort a list of alignments by score\nfirst_al  = needle.NeedlemanWunsch(seq1, seq2)\nsecond_al = needle.NeedlemanWunsch(seq3, seq4)\n\nfor align in sorted([first_al, second_al], reverse=True):\n    print(align)\n\n```\n\n\n\n## Install\n```bash\npip install minineedle\n```\n\n\n## Classes\n\n### NeedlemanWunsch\nNeedleman-Wunsch alignment class. It has the following attributes:\n- seq1\n- seq2     \n- alseq1   \n- alseq2\n- nmatrix   \n- pmatrix   \n- smatrix  \n- score    \n- identity\n- gap_character\n\nTo create the instance you have to provide two iterable objects with elements that can be compared with "==".\n\n### SmithWaterman\nSmith-Waterman alignment class. It has the following attributes:\n- seq1\n- seq2     \n- alseq1   \n- alseq2\n- nmatrix   \n- pmatrix   \n- smatrix  \n- score    \n- identity\n\nTo create the instance you have to provide two iterable objects with elements that can be compared with "==".\n\n### ScoreMatrix\nWith this class you can define your own score matrices. It has three attributes:\n- match\n- miss\n- gap\n\n\n## Methods\n### align()\nPerforms the alignment.\n\n### get_score()\nReturns the score of the alignment. It runs align() if it has not been done yet.\n\n### change_matrix(newmatrix)\nTakes a ScoreMatrix object and updates the matrix for the alignment. You still have to run it calling `align()`.\n\n### get identity()\nReturns the % of identity (rounded with 2 decimal points).\n\n### get_almatrix()\nReturn the alignment matrix as a list of lists.\n',
    'author': 'S. Castillo-Lara',
    'author_email': 'sergiocastillo@ub.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/scastlara/minineedle',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
