"""Find which shape (province, city or barangay) a map point falls in. Uses numpy only."""

import json

import numpy as np


def rings_of(geometry_json):
    """All rings of a Polygon or MultiPolygon, as numpy arrays of (longitude, latitude)."""
    geometry = json.loads(geometry_json)
    polygons = (
        [geometry["coordinates"]]
        if geometry["type"] == "Polygon"
        else geometry["coordinates"]
    )
    return [np.asarray(ring, dtype=float) for polygon in polygons for ring in polygon]


def inside(rings, lon, lat):
    """True for each point inside the shape. Holes count as outside (even-odd rule)."""
    result = np.zeros(len(lon), dtype=bool)
    for ring in rings:
        x1, y1 = ring[:, 0], ring[:, 1]
        x2, y2 = np.roll(x1, 1), np.roll(y1, 1)
        for a, b, c, d in zip(x1, y1, x2, y2):
            crosses = (b > lat) != (d > lat)
            if not crosses.any():
                continue
            with np.errstate(divide="ignore", invalid="ignore"):
                x_at = (c - a) * (lat - b) / (d - b) + a
            result ^= crosses & (lon < x_at)
    return result


def assign(lon, lat, shapes):
    """Give each point the name of the first shape it falls in, or None.

    shapes is a list of (name, geometry_json), in the order to try. Put cities before provinces,
    because a city's shape sits inside its province's shape.
    """
    lon, lat = np.asarray(lon, dtype=float), np.asarray(lat, dtype=float)
    names = np.full(len(lon), None, dtype=object)
    for name, geometry_json in shapes:
        rings = rings_of(geometry_json)
        corners = np.vstack(rings)
        (x0, y0), (x1, y1) = corners.min(axis=0), corners.max(axis=0)
        todo = (names == None) & (lon >= x0) & (lon <= x1) & (lat >= y0) & (lat <= y1)  # noqa: E711
        if todo.any():
            idx = np.flatnonzero(todo)
            hit = inside(rings, lon[idx], lat[idx])
            names[idx[hit]] = name
    return names
