import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import scipy.sparse as sp

def get_matrix_triad(coo_matrix, data=False):
    # 检查类型
    if not sp.isspmatrix_coo(coo_matrix):
        # 转化为三元组表示的稀疏矩阵
        coo_matrix = sp.coo_matrix(coo_matrix)
    # 分别为 矩阵行，矩阵列及对应的矩阵值
    temp = np.vstack((coo_matrix.row, coo_matrix.col)).transpose()
    return temp.tolist()
def get_num(statistics_path='./statistics.csv'):
    raw_data = pd.read_csv(statistics_path, sep=',')
    return len(raw_data)
def get_info(node_id, statistics_path='./statistics.csv'):
    raw_data = pd.read_csv(statistics_path, sep=',')
    # node_classes = raw_data.iloc[:, 1:2]
    node_classes = raw_data
    node_label=""
    node_title=""
    # print("node_classes shape: ", node_classes.shape)
    for i in range(len(node_classes)):
        if(int(node_classes["node_id"][i])==node_id):
            node_label = node_classes["node_class"][i]
            node_title = node_classes["title"][i]
            break
    return node_label, node_title
def get_label_list(statistics_path='./statistics.csv'):
    label_list = []
    raw_data = pd.read_csv(statistics_path, sep=',')
    # node_classes = raw_data.iloc[:, 1:2]
    node_classes = raw_data
    # print("node_classes shape: ", node_classes.shape)
    for i in range(len(node_classes)):
        label_list.append(node_classes["node_class"][i])
    return label_list
def get_adj(adj, cite_path='./ME.cites'):
    raw_data_cites = pd.read_csv(cite_path, sep='\t', header=None)
    for i in range(len(raw_data_cites)):
        index_i = raw_data_cites[0][i] - 1
        index_j = raw_data_cites[1][i] - 1
        adj[index_i][index_j] = 1
        adj[index_j][index_i] = 1
    adj = adj.astype(np.int16)
    return adj



statistics_path = './statistics.csv'
cite_path = './cites.csv'
num_nodes = get_num(statistics_path)
adj = np.zeros((num_nodes, num_nodes))
adj = get_adj(adj, cite_path)
G = nx.Graph()
H = nx.path_graph(adj.shape[0])
G.add_nodes_from(H)
edags = get_matrix_triad(adj)
G.add_edges_from(edags)
label_list = get_label_list(statistics_path)
colors = label_list
nx.draw(G, pos=nx.spring_layout(G), node_color=colors, with_labels=True)
plt.show()

print('number of nodes', G.number_of_nodes())
print('number of edges', G.number_of_edges())


# node_id = 38
# node_label, node_title = get_label(node_id)
# print("label=%s, title=\'%s\'" % (node_label, node_title))
