
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
                # ... добавить в конец очереди...
                queue.append(child)
                # ... и пометить как посещённые
                visited[child] = True
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
    data_as_string = """<?xml version="1.0" encoding="UTF-8" ?>
<page>
    <item name = 'a_1'>
        <item name="a_1_b_1"></item>
        <item name="a_1_b_2">
            <item name="a_1_b_2_c_1"></item>
            <item name="a_1_b_2_c_2"></item>
            <item name="a_1_b_2_c_3"></item>
        </item>
        <item name="a_1_b_3">
            <item name="a_1_b_3_c_1"></item>
        </item>
    </item>
    <item name = 'a_2'>
        <item name="a_2_b_1"></item>
        <item name="a_2_b_2">
            <item name="a_2_b_2_c_1"></item>
            <item name="a_2_b_2_c_2"></item>
            <item name="a_2_b_2_c_3"></item>
        </item>
        <item name="a_2_b_3"></item>
        <item name="a_2_b_4">
            <item name="a_2_b_4_c_1"></item>
            <item name="a_2_b_4_c_2"></item>
        </item>
        <item name="a_2_b_5"></item>
    </item>
    <item name = 'a_3'>
        <item name="a_3_b_1"></item>
    </item>
    <item name = 'a_4'>
        <item name="a_4_b_1">
            <item name="a_4_b_1_c_1"></item>
            <item name="a_4_b_1_c_2"></item>
        </item>
        <item name="a_4_b_2">
            <item name="a_4_b_2_c_1"></item>
        </item>
    </item>
</page>
    """
    xml_path = 'test_page2.xml'
    #tree = ET.parse(xml_path)
    # xml_page: ET.Element = tree.getroot()
    xml_page = ET.fromstring(data_as_string)
    res = read_tree(xml_page)
    assert res == OUTPUT
