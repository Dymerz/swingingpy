Swinging Door Algorithm real time compression
==============================================

This module is the implementation of the swinging door algorithm in Python.


Install
--------

    pip install swingingpy

Usage
------
```py
    from swingingpy import SwingingDoor, Cpoint

    comp_dev = 1
    comp_max = 5
    original = CPoint(0, 0)
    snapshot = None

    sd = SwingingDoor(
        comp_dev=comp_dev, 
        comp_max=comp_max, 
        original=original, 
        snapshot=snapshot
    )

    points = [
        CPoint(1, 0),
        CPoint(2, 5),
        CPoint(3, 6),
    ]

    for p in points:
        point = compressor.check(p)

        if point:
            print(f"Compressed {point}")
        else:
            print(f"Uncompressed {point}")
```


Sources:
-------
- https://github.com/gfoidl/DataCompression
- https://www.mathworks.com/matlabcentral/fileexchange/39081-data-compression-by-removing-redundant-points?focused=3774824&tab=function
- https://www.youtube.com/watch?v=89hg2mme7S0
- https://www.researchgate.net/publication/317119512_The_Research_and_Improvement_of_SDT_Algorithm_for_Historical_Data_in_SCADA
