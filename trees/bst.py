from collections import deque

class Node:

    def __init__(self, key, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent

    def insert(self, root, key):
        if root is None:
            return Node(key)
        elif key < root.key:
            root.left = self.insert(root.left, key)
        elif key > root.key:
            root.right = self.insert(root.right, key)
        return root

    def search(self, root, key):
        if root is None or key == root.key:
            return root
        elif key < root.key:
            return self.search(root.left, key)
        else:
            return self.search(root.right, key)

    def findmin(self, root):
        """Находит узел с минимальным ключом в поддереве"""
        if root is None:
            return None
        current = root
        while current.left:
            current = current.left
        return current

    def findmax(self, root):
        """Находит узел с максимальным ключом в поддереве"""
        if root is None:
            return None
        current = root
        while current.right:
            current = current.right
        return current

    def delete(self, root, key):
        if root is None:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Нашли узел для удаления
            if root.left is None and root.right is None:
                # Узел без детей
                return None
            elif root.left is None:
                # Узел с одним правым ребенком
                if root.right:
                    root.right.parent = root.parent
                return root.right
            elif root.right is None:
                # Узел с одним левым ребенком
                if root.left:
                    root.left.parent = root.parent
                return root.left
            else:
                # Узел с двумя детьми
                # Находим минимальный узел в правом поддереве
                min_node = self.findmin(root.right)
                if min_node:
                    # Копируем значение минимального узла
                    root.key = min_node.key
                    # Удаляем минимальный узел из правого поддерева
                    root.right = self.delete(root.right, min_node.key)
                else:
                    # Если правого поддерева нет, используем максимальный из левого
                    max_node = self.findmax(root.left)
                    if max_node:
                        root.key = max_node.key
                        root.left = self.delete(root.left, max_node.key)

        return root

    def inorder(self, root, result=None):
        """Исправленный inorder, который возвращает список"""
        if result is None:
            result = []
        if root is not None:
            self.inorder(root.left, result)
            result.append(root.key)
            self.inorder(root.right, result)
        return result

    def preorder(self, root, result=None):
        """Preorder с возвратом результата"""
        if result is None:
            result = []
        if root is not None:
            result.append(root.key)
            self.preorder(root.left, result)
            self.preorder(root.right, result)
        return result

    def postorder(self, root, result=None):
        """Postorder с возвратом результата"""
        if result is None:
            result = []
        if root is not None:
            self.postorder(root.left, result)
            self.postorder(root.right, result)
            result.append(root.key)
        return result

    def bfs(self, root):
        """BFS, который возвращает список"""
        result = []
        if root is None:
            return result
        queue = deque([root])
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def height(self, root):
        """Вычисление высоты дерева"""
        if root is None:
            return -1
        left_height = self.height(root.left)
        right_height = self.height(root.right)
        return 1 + max(left_height, right_height)

    def print_tree_visual(self, root, level=0, prefix="Root: "):
        """Визуализация дерева (корень сверху)"""
        if root is None:
            print("Дерево пустое")
            return

        # Сначала выводим правую ветку (она будет слева в выводе)
        if root.right:
            self.print_tree_visual(root.right, level + 1, "┌── ")

        # Выводим текущий узел
        indent = "    " * level
        print(indent + prefix + str(root.key))

        # Затем выводим левую ветку
        if root.left:
            self.print_tree_visual(root.left, level + 1, "└── ")


def test_bst():
    """Тестирование обычного бинарного дерева поиска"""
    print("=" * 50)
    print("ТЕСТ ОБЫЧНОГО BST ДЕРЕВА")
    print("=" * 50)

    # Создаем экземпляр для вызова методов
    bst = Node(0)

    # Начинаем с пустого дерева
    root = None

    # Вставка элементов
    test_keys = [50, 30, 70, 20, 40, 60, 80, 10, 90]
    print("1. Вставляем элементы:", test_keys)

    for key in test_keys:
        root = bst.insert(root, key)
        print(f"   Вставил {key}", end="")
        height = bst.height(root)
        print(f" - высота дерева: {height}")

    # Проверка обходов
    print("\n2. Проверка обходов:")

    # Inorder обход
    inorder_result = bst.inorder(root)
    print("   Inorder (должен быть отсортирован):", inorder_result)

    # Проверка отсортированности
    if inorder_result == sorted(inorder_result):
        print("   ✓ Дерево корректно отсортировано")
    else:
        print("   ✗ Нарушена сортировка дерева")

    # BFS обход
    bfs_result = bst.bfs(root)
    print("   BFS (по уровням):", bfs_result)

    # Проверка поиска
    print("\n3. Тест поиска:")
    search_tests = [
        (30, "существующий в левом поддереве"),
        (70, "существующий в правом поддереве"),
        (55, "несуществующий"),
        (90, "существующий лист")
    ]

    for key, description in search_tests:
        result = bst.search(root, key)
        if result:
            print(f"   Ключ {key} ({description}) найден")
        else:
            print(f"   Ключ {key} ({description}) не найден")

    # Высота дерева
    print(f"\n4. Высота дерева: {bst.height(root)}")

    # Визуализация дерева
    print("\n5. Визуализация дерева:")
    bst.print_tree_visual(root)

    # Тест удаления
    print("\n6. Тест удаления:")

    # Удаляем лист
    print("   Удаляем лист 10:")
    root = bst.delete(root, 10)
    print(f"   Inorder после удаления: {bst.inorder(root)}")
    print(f"   Высота после удаления 10: {bst.height(root)}")

    # Удаляем узел с одним ребенком
    print("\n   Удаляем узел с одним ребенком 20:")
    root = bst.delete(root, 20)
    print(f"   Inorder после удаления: {bst.inorder(root)}")
    print(f"   Высота после удаления 20: {bst.height(root)}")

    # Удаляем узел с двумя детьми
    print("\n   Удаляем узел с двумя детьми 50 (корень):")
    root = bst.delete(root, 50)
    print(f"   Inorder после удаления: {bst.inorder(root)}")
    print(f"   Высота после удаления 50: {bst.height(root)}")

    # Проверяем поиск после удаления
    print("\n7. Проверка поиска после удаления:")
    for key in [50, 30, 60, 10]:
        result = bst.search(root, key)
        if result:
            print(f"   Ключ {key} найден")
        else:
            print(f"   Ключ {key} не найден")

    print("\n8. Финальное дерево:")
    bst.print_tree_visual(root)

    return root


if __name__ == "__main__":
    test_bst()