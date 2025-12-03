from bst import Node


class RB_Node(Node):
    RED = "RED"
    BLACK = "BLACK"

    def __init__(self, key, parent=None, color=RED):
        super().__init__(key, parent)
        self.color = color

    def get_root(self):
        """Получить корень дерева"""
        node = self
        while node.parent:
            node = node.parent
        return node

    def black_height(self, node=None):
        """Вычисляет черную высоту поддерева"""
        if node is None:
            node = self

        if node is None:
            return 1  # NIL узлы считаются черными

        left_bh = self.black_height(node.left) if node.left else 0
        right_bh = self.black_height(node.right) if node.right else 0

        if left_bh != right_bh:
            return -1  # Ошибка балансировки

        # Увеличиваем черную высоту, если текущий узел черный
        return left_bh + (1 if node.color == RB_Node.BLACK else 0)

    def insert(self, key):
        """Вставка ключа в дерево"""
        if key < self.key:
            if self.left is None:
                self.left = RB_Node(key, self, RB_Node.RED)
                return self.left.fix_insertion()
            else:
                return self.left.insert(key)
        elif key > self.key:
            if self.right is None:
                self.right = RB_Node(key, self, RB_Node.RED)
                return self.right.fix_insertion()
            else:
                return self.right.insert(key)
        # Ключ уже существует
        return self.get_root()

    def fix_insertion(self):
        """Исправление свойств красно-черного дерева после вставки"""
        node = self

        while node.parent is not None and node.parent.color == RB_Node.RED:
            parent = node.parent
            grandparent = parent.parent

            if grandparent is None:
                break

            if parent == grandparent.left:
                uncle = grandparent.right

                # Случай 1: дядя красный
                if uncle is not None and uncle.color == RB_Node.RED:
                    parent.color = RB_Node.BLACK
                    uncle.color = RB_Node.BLACK
                    grandparent.color = RB_Node.RED
                    node = grandparent
                else:
                    # Случай 2: узел - правый потомок
                    if node == parent.right:
                        node = parent
                        self._left_rotate(node)
                        parent = node.parent
                        grandparent = parent.parent if parent else None

                    # Случай 3: узел - левый потомок
                    if parent:
                        parent.color = RB_Node.BLACK
                    if grandparent:
                        grandparent.color = RB_Node.RED
                        self._right_rotate(grandparent)
            else:
                # Симметричный случай: parent - правый потомок
                uncle = grandparent.left

                # Случай 1: дядя красный
                if uncle is not None and uncle.color == RB_Node.RED:
                    parent.color = RB_Node.BLACK
                    uncle.color = RB_Node.BLACK
                    grandparent.color = RB_Node.RED
                    node = grandparent
                else:
                    # Случай 2: узел - левый потомок
                    if node == parent.left:
                        node = parent
                        self._right_rotate(node)
                        parent = node.parent
                        grandparent = parent.parent if parent else None

                    # Случай 3: узел - правый потомок
                    if parent:
                        parent.color = RB_Node.BLACK
                    if grandparent:
                        grandparent.color = RB_Node.RED
                        self._left_rotate(grandparent)

        # Корень всегда черный
        root = self.get_root()
        root.color = RB_Node.BLACK
        return root

    def _left_rotate(self, x):
        """Левый поворот вокруг узла x"""
        y = x.right
        if y is None:
            return

        # Поворот
        x.right = y.left
        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            # x был корнем
            pass
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        """Правый поворот вокруг узла y"""
        x = y.left
        if x is None:
            return

        # Поворот
        y.left = x.right
        if x.right is not None:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is None:
            # y был корнем
            pass
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def left_rotate(self):
        """Левый поворот (публичный интерфейс)"""
        pivot = self.right
        if pivot is None:
            return self

        # Сохраняем родителя
        parent = self.parent

        # Выполняем поворот
        self.right = pivot.left
        if pivot.left:
            pivot.left.parent = self

        pivot.left = self
        self.parent = pivot
        pivot.parent = parent

        # Обновляем ссылку у родителя
        if parent:
            if self == parent.left:
                parent.left = pivot
            else:
                parent.right = pivot

        return pivot

    def right_rotate(self):
        """Правый поворот (публичный интерфейс)"""
        pivot = self.left
        if pivot is None:
            return self

        # Сохраняем родителя
        parent = self.parent

        # Выполняем поворот
        self.left = pivot.right
        if pivot.right:
            pivot.right.parent = self

        pivot.right = self
        self.parent = pivot
        pivot.parent = parent

        # Обновляем ссылку у родителя
        if parent:
            if self == parent.left:
                parent.left = pivot
            else:
                parent.right = pivot

        return pivot

    def search(self, key):
        """Поиск ключа в дереве"""
        if key == self.key:
            return self
        elif key < self.key and self.left:
            return self.left.search(key)
        elif key > self.key and self.right:
            return self.right.search(key)
        return None

    def print_tree_visual(self, level=0, prefix="Root: "):
        """Визуализация дерева"""
        # Сначала выводим правую ветку
        if self.right:
            self.right.print_tree_visual(level + 1, "┌── ")

        # Выводим текущий узел
        indent = "    " * level
        color_char = 'R' if self.color == RB_Node.RED else 'B'
        node_info = f"{self.key}({color_char})"
        print(indent + prefix + node_info)

        # Затем выводим левую ветку
        if self.left:
            self.left.print_tree_visual(level + 1, "└── ")

    def validate_rb_tree(self):
        """Проверка свойств красно-черного дерева"""
        violations = []

        def _validate(node):
            if node is None:
                return 1, True  # Черная высота, валидно

            # Проверяем свойство красного узла
            if node.color == RB_Node.RED:
                if (node.left and node.left.color == RB_Node.RED) or \
                        (node.right and node.right.color == RB_Node.RED):
                    return 0, False

            # Рекурсивно проверяем детей
            left_bh, left_valid = _validate(node.left)
            right_bh, right_valid = _validate(node.right)

            if not left_valid or not right_valid:
                return 0, False

            # Проверяем черную высоту
            if left_bh != right_bh:
                return 0, False

            # Возвращаем черную высоту этого поддерева
            current_bh = left_bh + (1 if node.color == RB_Node.BLACK else 0)
            return current_bh, True

        # Проверка 1: корень должен быть черным
        root = self.get_root()
        if root.color != RB_Node.BLACK:
            violations.append("Корень не черный")

        # Проверка 2: все свойства RB-дерева
        _, is_valid = _validate(root)
        if not is_valid:
            violations.append("Нарушены свойства красно-черного дерева")

        return violations


def test_rb():
    print("\n" + "=" * 50)
    print("ТЕСТ КРАСНО-ЧЕРНОГО ДЕРЕВА")
    print("=" * 50)

    # Тест 1: Простая вставка
    print("1. Создаем и тестируем красно-черное дерево")

    # Создаем корень
    root = RB_Node(10, color=RB_Node.BLACK)
    print(f"   Создан корень: {root.key} (черный)")

    # Вставляем элементы
    keys_to_insert = [5, 15, 3, 7, 12, 18, 2, 4, 6, 8, 11, 14, 17, 20]

    for key in keys_to_insert:
        print(f"   Вставляем {key}...", end="")
        root = root.insert(key)
        root = root.get_root()
        violations = root.validate_rb_tree()
        if not violations:
            print(" ✓")
        else:
            print(" ✗")
            print(f"     Ошибки: {violations}")

    print(f"\n2. Корень дерева: {root.key} (цвет: {root.color})")

    print("\n3. Визуализация дерева:")
    root.print_tree_visual()

    print("\n4. Проверка свойств:")
    violations = root.validate_rb_tree()
    if not violations:
        print("   ✓ Все свойства красно-черного дерева выполнены")
    else:
        print("   ✗ Нарушены свойства:")
        for v in violations:
            print(f"     - {v}")

    print(f"\n5. Черная высота дерева: {root.black_height()}")

    print("\n6. Тест поиска:")
    test_keys = [10, 5, 15, 3, 100, 7, 12]
    for key in test_keys:
        node = root.search(key)
        if node:
            color = 'красный' if node.color == RB_Node.RED else 'черный'
            print(f"   Ключ {key}: найден, цвет = {color}")
        else:
            print(f"   Ключ {key}: не найден")

    print("\n7. Проверка сортировки (inorder traversal):")

    def inorder(node, result=None):
        if result is None:
            result = []
        if node:
            inorder(node.left, result)
            result.append(node.key)
            inorder(node.right, result)
        return result

    sorted_keys = inorder(root)
    print(f"   Отсортированные ключи: {sorted_keys}")

    is_sorted = all(sorted_keys[i] <= sorted_keys[i + 1] for i in range(len(sorted_keys) - 1))
    if is_sorted:
        print("   ✓ Дерево корректно отсортировано")
    else:
        print("   ✗ Нарушена сортировка")

    return root


if __name__ == "__main__":
    # Запуск теста
    test_rb()