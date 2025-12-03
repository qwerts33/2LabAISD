from bst import Node
import random
import matplotlib.pyplot as plt
import math


def build_bst(keys):
    if not keys:
        return None
    root = Node(keys[0])
    for key in keys[1:]:
        root.insert(root,key)
    return root

min_n = 100
max_n = 10000
step = 100
num_trials = 20

n_values = list(range(min_n, max_n + 1, step))
heights = []

for n in n_values:
    total_height = 0
    print(f"Обработка {n} ключей.")
    for _ in range(num_trials):
        keys = random.sample(range(1, 1000000), n)
        root = build_bst(keys)
        total_height += root.height(root)
    heights.append(total_height / num_trials)


plt.figure(figsize=(12, 8))
plt.plot(n_values, heights, 'b-', label='Экспериментальная высота', linewidth=2)

plt.plot(n_values, [2.2 * math.log2(n) for n in n_values], 'g--', label='2.2 log₂(n)')

plt.xlabel('Количество ключей (n)')
plt.ylabel('Высота дерева')
plt.title('Зависимость высоты BST от количества ключей')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()


print("Асимптотика высоты BST:")
print("- В худшем случае (несбалансированное дерево): O(n)")
print("- В среднем случае для случайных ключей: O(log n)")
print("- Эксперимент подтверждает логарифмический рост высоты")