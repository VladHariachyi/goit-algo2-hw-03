import csv
from pathlib import Path
from BTrees.OOBTree import OOBTree
from typing import Callable
from timeit import timeit


def fill_object_with_contnet(
    storage: dict | OOBTree,
    callback: Callable[[dict | OOBTree, dict], None]
) -> None:
    with open(Path(__file__).parent / "generated_items_data.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            callback(
                storage,
                {
                    "id": row["ID"],
                    "name": row["Name"],
                    "category": row["Category"],
                    "price": float(row["Price"])
                }
            )

def add_item_to_dict(
    storage: dict,
    item: dict
) -> None:
    storage[item["id"]] = item   

def add_item_to_tree(
    storage: OOBTree,
    item: dict
) -> None:
    found_node_with_same_price = storage.get(item["price"])

    if found_node_with_same_price is None:
        # Set price as key to make correct work of tree.items(min, max)
        storage[item["price"]] = [item]
    else:
        found_node_with_same_price.append(item)


def range_query_dict(data: dict, min: int, max: int) -> list[dict]:
    result = []

    for item in data.values():
        if item["price"] >= min and item["price"] <= max:
            result.append(item)

    return result

def range_query_tree(data: OOBTree, min: int, max: int) -> list[dict]:
    result = []

    for items in data.items(min, max):
        result.extend(items)

    return result


if __name__ == "__main__":
    dict_storage = {}
    oob_tree_storage = OOBTree()

    fill_object_with_contnet(dict_storage, add_item_to_dict)
    fill_object_with_contnet(oob_tree_storage, add_item_to_tree)

    # Single call execution time

    dict_query_execution_time = timeit(
        stmt=lambda: range_query_dict(dict_storage, 100, 200),
        number=1
    )

    oob_tree_query_execution_time = timeit(
        stmt=lambda: range_query_tree(oob_tree_storage, 100, 200),
        number=1
    )

    print("---- Single query ----")
    print(f"Total range_query time for Dict {dict_query_execution_time:.8f} sec")
    print(f"Total range_query time for OOBTree: {oob_tree_query_execution_time:.8f} sec")

    # 100 calls

    dict_query_execution_time = timeit(
        stmt=lambda: [range_query_dict(dict_storage, 100, 200) for _ in range(100)],
        number=1
    )
    
    oob_tree_query_execution_time = timeit(
        stmt=lambda: [range_query_tree(oob_tree_storage, 100, 200) for _ in range(100)],
        number=1
    )

    print("---- 100 queries ----")

    print(f"Total range_query time for Dict {dict_query_execution_time:.8f} sec")
    print(f"Total range_query time for OOBTree: {oob_tree_query_execution_time:.8f} sec")