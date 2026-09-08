from graph import build_graph
from max_flow import edmonds_karp_max_flow

positions = {
    0: (0, 0), # T1
    1: (5, 0), # T2
    #---------------
    2: (1, 1), # Storage 1
    3: (4, 1), # Storage 2
    4: (1, -1), # Storage 3
    5: (4, -1), # Storage 4
    #--------------------
    6: (-3, 2), # store 1
    7: (-1.5, 2), # store 2
    8: (0, 2), # store 3
    #---------------------
    9: (2, 2), # store 4
    10: (4, 2), # store 5
    11: (6, 2), # store 6
    #----------------------
    12: (-3, -2), # store 7
    13: (-1.5, -2), # store 8
    14: (0, -2), # store 9
    #----------------------
    15: (2, -2), # store 10
    16: (3.5, -2), # store 11
    17: (5, -2), # store 12
    18: (6.5, -2), # store 13
    19: (8, -2), # store 14
}

labels = {
    0: "Термінал 1",
    1: "Термінал 2",
    2: "Склад 1",
    3: "Склад 2",
    4: "Склад 3",
    5: "Склад 4",
    6: "Магазин 1",
    7: "Магазин 2",
    8: "Магазин 3",
    9: "Магазин 4",
    10: "Магазин 5",
    11: "Магазин 6",
    12: "Магазин 7",
    13: "Магазин 8",
    14: "Магазин 9",
    15: "Магазин 10",
    16: "Магазин 11",
    17: "Магазин 12",
    18: "Магазин 13",
    19: "Магазин 14",
}

base_capacity = [
    [0, 0, 25, 20, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # T1 (0)
    [0, 0, 0, 10, 15, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # T2 (1)
    [0, 0, 0, 0, 0, 0, 15, 10, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # S1 (2)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 10, 25, 0, 0, 0, 0, 0, 0, 0, 0], # S2 (3)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 15, 10, 0, 0, 0, 0, 0], # S3 (4)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 15, 5, 10], # S4 (5)
] + [[0] * 20 for _ in range(14)]

# Add source and sink for correct calculation the max flow
matrix_size = 22
capacity_matrix = [[0] * matrix_size for _ in range(matrix_size)]

for r in range(20):
    for c in range(20):
        capacity_matrix[r][c] = base_capacity[r][c]

# source for t1 and t2
capacity_matrix[20][0] = float('inf')
capacity_matrix[20][1] = float('inf')

# sink for each store
for store_idx in range(6, 20):
    capacity_matrix[store_idx][21] = float('inf')


if __name__ == "__main__":
    edges = []
    result_table = []

    # max flow is calculated via definition start and end points, in this case strart -> source, end -> sink
    flow_matrix = edmonds_karp_max_flow(capacity_matrix, 20, 21)

    # build graph
    # build term and storage deps
    for t_idx in [0, 1]:
        for s_idx in [2, 3, 4, 5]:
            cap = base_capacity[t_idx][s_idx]
            if cap > 0:
                actual_flow = max(0, flow_matrix[t_idx][s_idx])
                edges.append((t_idx, s_idx, actual_flow))

    # build storage and store deps
    for s_idx in [2, 3, 4, 5]:
        for m_idx in range(6, 20):
            cap = base_capacity[s_idx][m_idx]
            if cap > 0:
                actual_flow = max(0, flow_matrix[s_idx][m_idx])
                edges.append((s_idx, m_idx, actual_flow))

    # build table
    for t_idx in [0, 1]:
        terminal_name = labels[t_idx]
        
        for m_idx in range(6, 20):
            store_name = labels[m_idx]
            delivered = 0.0

            # storages
            for s_idx in [2, 3, 4, 5]:
                flow_t_s = max(0, flow_matrix[t_idx][s_idx])  # term -> storage
                flow_s_m = max(0, flow_matrix[s_idx][m_idx])  # storage -> store
                
                # general stream to storage for all terminals
                total_s_inflow = sum(max(0, flow_matrix[t][s_idx]) for t in [0, 1])

                # move product to store if it exists in storage
                if flow_t_s > 0 and flow_s_m > 0 and total_s_inflow > 0:
                    # calculates how many products were delivered from term to storage 
                    # and from storage to specific store
                    share = flow_t_s / total_s_inflow
                    delivered += flow_s_m * share

            result_table.append({
                "terminal": terminal_name,
                "store": store_name,
                "flow": round(delivered, 2)
            })


    print(f"{'Термінал':<12} | {'Магазин':<12} | {'Фактичний Потік':<10}")
    print("-" * 42)

    for row in result_table:
        print(f"{row['terminal']:<12} | {row['store']:<12} | {row['flow']:<10}") 

    build_graph(edges, positions, labels)



    # 1. Термінал 1 забезпечує найблільший потік товарів в магазини (60 товарів), т/к термінал 2 тільки
    # доставляє 55 товарів

    # 2. Найменшу пропускну здатність мають ребра між складами та магазинами 
    # (від 5 до 10 одиниць, наприклад: Склад 4 -> Магазин 13 має 5 од., 
    # Склад 1 -> Магазин 2 має 10 од.).
    # Це впливає на загальний потік, оскільки обмежена кількість товару зі складу 
    # повністю вичерпується на перших за порядком маршрутах, а наступним магазинам 
    # (незалежно від їхньої пропускної здатності) залишається 0 одиниць товару.

    # 3. Магазини 3, 9, 12, 13, 14 отримали найменшу к-сть товарів (0 одиниць)
    # Треба збиільшити пропусну здатність між Складами 1, 3, 4 і Магазинами, також
    # збільшити пропускну здатність терміналів т/к вони вже переповнені

    # 4. Так є, тому що термінали повністю завантажені і не здатні обробити більший обсяг товару
    # а деякі магазини так і не отримали товару

