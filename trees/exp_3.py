import math
import matplotlib.pyplot as plt
from avl import AVL_Node
from rb import RB_Node


def get_tree_height(node):
    """Рекурсивно вычисляет высоту дерева"""
    if node is None:
        return 0
    return 1 + max(get_tree_height(node.left), get_tree_height(node.right))


# Параметры эксперимента
min_keys = 100
max_keys = 10000
step = 100

key_counts = list(range(min_keys, max_keys + 1, step))
avl_heights = []
rbt_heights = []
avl_upper_bound = []
avl_lower_bound = []
rbt_upper_bound = []
rbt_lower_bound = []

for n in key_counts:
    print(f"Обрабатывается {n} ключей...")

    avl_height_sum = 0
    rbt_height_sum = 0
    keys = list(range(1, n + 1))

    avl_root = AVL_Node(keys[0])
    for key in keys[1:]:
        avl_root = avl_root.insert(key)

    rbt_root = RB_Node(keys[0])
    for key in keys[1:]:
        rbt_root.insert(key)
        rbt_root = rbt_root.get_root()

    avl_heights.append(get_tree_height(avl_root))
    rbt_heights.append(get_tree_height(rbt_root))

    avl_upper_bound.append(1.44 * math.log2(n + 1))
    avl_lower_bound.append(math.log2(n + 1))

    rbt_upper_bound.append(2 * math.log2(n + 1))
    rbt_lower_bound.append(math.log2(n + 1))

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
plt.plot(key_counts, avl_heights, 'b-', label='Экспериментальная высота AVL', linewidth=2)
plt.plot(key_counts, avl_upper_bound, 'r--', label='Теоретическая верхняя оценка AVL', linewidth=1.5)
plt.plot(key_counts, avl_lower_bound, 'g--', label='Теоретическая нижняя оценка AVL', linewidth=1.5)
plt.xlabel('Количество ключей')
plt.ylabel('Высота дерева')
plt.title('Зависимость высоты AVL дерева\n(монотонно возрастающие ключи)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(key_counts, rbt_heights, 'b-', label='Экспериментальная высота RBT', linewidth=2)
plt.plot(key_counts, rbt_upper_bound, 'r--', label='Теоретическая верхняя оценка RBT', linewidth=1.5)
plt.plot(key_counts, rbt_lower_bound, 'g--', label='Теоретическая нижняя оценка RBT', linewidth=1.5)
plt.xlabel('Количество ключей')
plt.ylabel('Высота дерева')
plt.title('Зависимость высоты красно-черного дерева\n(монотонно возрастающие ключи)')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"\nСтатистика для {max_keys} ключей:")
print(f"AVL дерево - экспериментальная высота: {avl_heights[-1]:.2f}")
print(f"AVL дерево - теоретическая верхняя оценка: {avl_upper_bound[-1]:.2f}")
print(f"AVL дерево - теоретическая нижняя оценка: {avl_lower_bound[-1]:.2f}")
print(f"Красно-черное дерево - экспериментальная высота: {rbt_heights[-1]:.2f}")
print(f"Красно-черное дерево - теоретическая верхняя оценка: {rbt_upper_bound[-1]:.2f}")
print(f"Красно-черное дерево - теоретическая нижняя оценка: {rbt_lower_bound[-1]:.2f}")