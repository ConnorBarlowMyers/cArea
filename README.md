# cArea

Creates cAreas at random within an fArea. Brute force approach and grid based optimisation both tried.

Things to sort:

- Conversion between latlong and m, circle rad defined in m while fArea in LL
- GridSweeper method getting hung up on lowerleft quadrant
- Large memory usage for grid-based approach when the fArea gets large.
