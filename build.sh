#!/bin/bash
python3 setup.py sdist bdist_wheel
python3 -m pip install dist/swingingpy-0.0.1-py3-none-any.whl

exit 0
