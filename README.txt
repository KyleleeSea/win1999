Progress Update:
- Implemented three pathing algorithms for enemy
    - One backtracking algorithm (depth-first-first). No references needed.
    - One path following algorithm. No references needed.
    - One player following algorithm utilizing player row & col as
        heuristic. No references needed.
- Implemented triggers and behavior for each algorithm.
    - Enemy starts off "wandering" (backtracking), until it finds the
         "player shadow" where it will utilize the path following algorithm.
         If in range of player, following algorithm will be activated for
         20 seconds.
- Created "player shadow" mechanics.
- Fixed maze generation bug (maze generation now fully functional).
    (No references needed)
- Fixed player movement bug. Player movement now fully functional.
- Dynamic background audio scaffolding. 

Additional note: Please see google drive "TP1 Proposal Updated" doc for
    updated design doc.