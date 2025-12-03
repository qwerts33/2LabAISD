from bst import test_bst
from avl import test_avl
from rb import test_rb

def run_all_tests():
    print("ЗАПУСК ВСЕХ ТЕСТОВ ДЕРЕВЬЕВ")
    print("=" * 60)

    print("\n" + "=" * 50)
    bst_root = test_bst()

    try:
        from avl import test_avl
        avl_root = test_avl()
    except ImportError:
        print("\nФайл avl.py не найден, тест AVL пропущен")

    try:
        from rb import test_rb
        rb_root = test_rb()
    except ImportError:
        print("\nФайл rb_tree.py не найден, тест RB пропущен")

    print("\n" + "=" * 60)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")


if __name__ == "__main__":
    run_all_tests()