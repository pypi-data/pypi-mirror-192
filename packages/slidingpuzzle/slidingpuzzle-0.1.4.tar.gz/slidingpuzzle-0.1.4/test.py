import json
from tqdm import tqdm
from slidingpuzzle import *
#b=from_rows([0,1,5],[4,6,7],[2,8,3])
# b=from_rows([2, 1, 3], [4, 5, 6], [7, 8, 0])
# s1 = search(b, heuristic=linear_conflict_distance)
# s2 = search(b, heuristic=manhattan_distance)
# print("true distance:", len(s2.solution))
# print("our distance:", len(s1.solution))


with open("datasets/examples_4x4.json", "rt") as fp:
    db = json.load(fp)

delta = 0

for i, (board, solution) in tqdm(enumerate(db), total=len(db)):
    expected = len(solution)
    board = from_rows(*board)
    actual = linear_conflict_distance(board)
    delta += expected - actual
    assert expected >= actual, f"{i}: {board}"

print("avg delta:", round(delta / len(db), 2))