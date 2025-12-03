from bst import Node


class AVL_Node(Node):
    def __init__(self, key, parent=None):
        super().__init__(key, parent)
        self.height = 1

    def update_height(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1

    def get_balance(self):
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

    def rotate_left(self):
        new_root = self.right
        self.right = new_root.left
        if new_root.left:
            new_root.left.parent = self
        new_root.left = self
        new_root.parent = self.parent
        self.parent = new_root

        # Обновляем высоты в правильном порядке
        self.update_height()
        new_root.update_height()
        return new_root

    def rotate_right(self):
        new_root = self.left
        self.left = new_root.right
        if new_root.right:
            new_root.right.parent = self
        new_root.right = self
        new_root.parent = self.parent
        self.parent = new_root

        # Обновляем высоты в правильном порядке
        self.update_height()
        new_root.update_height()
        return new_root

    def rebalance(self):
        self.update_height()
        balance = self.get_balance()

        # Left Heavy
        if balance > 1:
            if self.left and self.left.get_balance() < 0:  # Left-Right case
                self.left = self.left.rotate_left()
            return self.rotate_right()  # Left-Left case

        # Right Heavy
        if balance < -1:
            if self.right and self.right.get_balance() > 0:  # Right-Left case
                self.right = self.right.rotate_right()
            return self.rotate_left()  # Right-Right case

        return self

    def insert(self, key):
        if key < self.key:
            if self.left is None:
                self.left = AVL_Node(key, self)
            else:
                self.left = self.left.insert(key)
        elif key > self.key:
            if self.right is None:
                self.right = AVL_Node(key, self)
            else:
                self.right = self.right.insert(key)
        else:
            return self

        return self.rebalance()

    def delete(self, key):
        # Базовый случай поиска узла
        if key < self.key:
            if self.left:
                self.left = self.left.delete(key)
        elif key > self.key:
            if self.right:
                self.right = self.right.delete(key)
        else:
            # Нашли узел для удаления
            if self.left is None and self.right is None:
                return None
            elif self.left is None:
                if self.right:
                    self.right.parent = self.parent
                return self.right
            elif self.right is None:
                if self.left:
                    self.left.parent = self.parent
                return self.left
            else:
                # Узел с двумя детьми
                successor = self.right
                while successor and successor.left:
                    successor = successor.left
                self.key = successor.key
                self.right = self.right.delete(successor.key)

        # Перебалансировка
        if self is None:
            return None
        return self.rebalance()

    # Исправленный метод search
    def search(self, key):
        # Переопределяем поиск для AVL дерева
        if key == self.key:
            return self
        elif key < self.key and self.left:
            return self.left.search(key)
        elif key > self.key and self.right:
            return self.right.search(key)
        return None

    def print_tree_visual(self, level=0, prefix="Root: "):
        """Визуализация дерева (корень сверху) с балансом"""
        if self is None:
            print("Дерево пустое")
            return

        # Сначала выводим правую ветку
        if self.right:
            self.right.print_tree_visual(level + 1, "┌── ")

        # Выводим текущий узел с балансом и высотой
        indent = "    " * level
        balance = self.get_balance()
        node_info = f"{self.key} (h:{self.height}, b:{balance})"
        print(indent + prefix + node_info)

        # Затем выводим левую ветку
        if self.left:
            self.left.print_tree_visual(level + 1, "└── ")


def test_avl():
    print("\n" + "=" * 50)
    print("ТЕСТ AVL ДЕРЕВА")
    print("=" * 50)

    avl_root = AVL_Node(50)

    print("1. Тест балансировки при последовательной вставке:")
    test_keys = [30, 70, 20, 40, 60, 80, 10, 90, 5]

    for key in test_keys:
        print(f"   Вставляем {key}", end="")
        avl_root = avl_root.insert(key)
        # Находим корень дерева
        while avl_root.parent:
            avl_root = avl_root.parent
        balance = avl_root.get_balance()
        print(f" - баланс корня: {balance}, высота: {avl_root.height}")
        if abs(balance) > 1:
            print("    Корень несбалансирован!")

    print("\n2. Проверка свойств AVL дерева:")

    def check_avl_balance(node):
        if node is None:
            return True

        balance = node.get_balance()
        if abs(balance) > 1:
            print(f"    Узел {node.key} несбалансирован (баланс: {balance})")
            return False

        left_ok = check_avl_balance(node.left)
        right_ok = check_avl_balance(node.right)
        return left_ok and right_ok

    if check_avl_balance(avl_root):
        print("    Все узлы сбалансированы (|баланс| ≤ 1)")

    print("\n3. Проверка сортировки:")
    sorted_keys = []

    def inorder_collect(node):
        if node:
            inorder_collect(node.left)
            sorted_keys.append(node.key)
            inorder_collect(node.right)

    inorder_collect(avl_root)
    print(f"   Inorder: {sorted_keys}")

    if sorted_keys == sorted(sorted_keys):
        print("     Дерево корректно отсортировано")
    else:
        print("     Нарушена сортировка дерева")

    print("\n4. Тест удаления элементов:")
    delete_keys = [40, 70]
    for key in delete_keys:
        print(f"   Удаляем {key}")
        if avl_root:
            avl_root = avl_root.delete(key)
            if avl_root:
                # Находим корень после удаления
                while avl_root.parent:
                    avl_root = avl_root.parent

    if avl_root:
        print(f"   Новый корень: {avl_root.key}")
        print(f"   Высота дерева: {avl_root.height}")
        print(f"   Баланс корня: {avl_root.get_balance()}")
    else:
        print("   Дерево пустое")

    print("\n5. Тест поиска:")
    search_keys = [50, 30, 100, 5]
    for key in search_keys:
        result = avl_root.search(key) if avl_root else None
        if result:
            print(f"   Ключ {key} найден, высота узла: {result.height}")
        else:
            print(f"   Ключ {key} не найден")

    print("\n6. Структура дерева:")
    if avl_root:
        avl_root.print_tree_visual()
    else:
        print("   Дерево пустое")

    return avl_root


if __name__ == "__main__":
    test_avl()