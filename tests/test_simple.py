import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

def test_import():
    import swingingpy

def test_simple():
    from swingingpy.compressor import SwingingDoor, CPoint

    comp_dev = 1
    comp_max = 5
    original = CPoint(0, 0)
    snapshot = None

    swing = SwingingDoor(
        comp_dev=comp_dev,
        comp_max=comp_max,
        original=original,
        snapshot=snapshot
    )

    expected_points = [5, 9, 13, 16, 19]
    points = []
    with open(dir_path + "/points.json") as _f:
        for _j in json.loads(_f.read()):
            points.append(CPoint(_j[0], _j[1]))

    result_points = []
    for _p in points:
        point = swing.check(_p)
        if point:
            result_points.append(point.get_x())

    assert result_points == expected_points
    assert swing.get_compression_ratio() == 75
