
def read_tree(start_node):
    res = ''
    visited = {}    # изначально список посещённых узлов пуст
    for node in start_node.iter():
        visited[node] = False
    queue = list()
    queue.append(start_node)              # начиная с узла-источника
    visited[start_node] = True
    while len(queue) != 0:             # пока очередь не пуста
        node = queue.pop()                 # извлечь первый элемент в очереди
        name = node.attrib.get('name')
        if name is not None:
             res += name + '\n'
        for child in node:     # все преемники текущего узла, ...
            if not visited[child]:       # ... которые ещё не были посещены ...
                queue.append(child)                # ... добавить в конец очереди...
                visited[child] = True            # ... и пометить как посещённые
    return res

OUTPUT = \
"""a_4
a_4_b_2
a_4_b_2_c_1
a_4_b_1
a_4_b_1_c_2
a_4_b_1_c_1
a_3
a_3_b_1
a_2
a_2_b_5
a_2_b_4
a_2_b_4_c_2
a_2_b_4_c_1
a_2_b_3
a_2_b_2
a_2_b_2_c_3
a_2_b_2_c_2
a_2_b_2_c_1
a_2_b_1
a_1
a_1_b_3
a_1_b_3_c_1
a_1_b_2
a_1_b_2_c_3
a_1_b_2_c_2
a_1_b_2_c_1
a_1_b_1
"""

def test_read_tree():
    from xml.etree import ElementTree as ET
    xml_path = 'test_page2.xml'
    tree = ET.parse(xml_path)
    xml_page: ET.Element = tree.getroot()
    res = read_tree(xml_page)
    assert res == OUTPUT
