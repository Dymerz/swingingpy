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

    points = [
        CPoint(1, 1),
        CPoint(2, 2),
        CPoint(3, 1),
        CPoint(4, 3),
        CPoint(5, 5),
    ]

    count = 0
    for p in points:
        point = swing.check(p)
        if point:
            count += 1

    assert swing.get_compression_ratio() == 80
    assert count == 1
