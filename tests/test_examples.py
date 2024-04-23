import glob
import shutil
import os

import nbformat
import pytest
from nbconvert.preprocessors import ExecutePreprocessor

EXAMPLES_PATH = 'docs/examples/'
example_notebooks = sorted(list(glob.glob(f'{EXAMPLES_PATH}/*.ipynb')))


@pytest.mark.parametrize("notebook", example_notebooks)
def test_notebook_exec(notebook):
    with open(notebook) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        try:
            assert ep.preprocess(
                nb,
                resources={'metadata': {'path': EXAMPLES_PATH}},
            ) is not None, f"Got empty notebook for {notebook}"
        except Exception:
            assert False, f"Failed executing {notebook}"

    for dir_to_clean in ['tmp', 'tmp2']:
        shutil.rmtree(
            os.path.join(EXAMPLES_PATH, dir_to_clean),
            ignore_errors=True,
            )
    if os.path.exists(
        res := os.path.join(EXAMPLES_PATH, 'existing_simulation/results.json')
    ):
        os.remove(res)
