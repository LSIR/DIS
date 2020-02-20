import numpy as np
import json
import pandas as pd
import operator
import networkx as nx
import matplotlib.pylab as plt
import matplotlib.colors as mcolors

def ex1_draw(G, measures):
    pos = nx.spring_layout(G,scale=3)
    _ = plt.figure(figsize=(25,10))


    edges = nx.draw_networkx_edges(G, pos, alpha=0.3)

    nodes = nx.draw_networkx_nodes(G, pos, node_size=250, cmap=plt.cm.rainbow,
                                   node_color=list(measures.values()),
                                   nodelist=list(measures.keys()))
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))

    cut_pos = {}
    for k,v in measures.items():
        if v>0.1:
            cut_pos[k] = k
            pos[k][1] += 0.15

    labels = nx.draw_networkx_labels(G, pos,labels=cut_pos,font_size=25)

    plt.title('Betweenness Centrality',fontsize=18)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()

def ex1_print_topn(dict_score,n):
    print("Betweeness centrality (unweighted):")
    print("-"*50)
    sorted_x = sorted(dict_score.items(), key=operator.itemgetter(1), reverse=True)
    for s in sorted_x[:n]:
        print(s[0].ljust(16),'\t\t','%.2f' % s[1])

def ex1_load_graph():
    mis_file = open('miserables.json')
    les_mis_json = json.load(mis_file)
    mis_links = pd.DataFrame(les_mis_json['links'])
    mis_nodes = pd.DataFrame(les_mis_json['nodes'])

    edge_list_df = pd.merge(mis_links,mis_nodes,left_on='source',right_index=True)
    edge_list_df = pd.merge(edge_list_df,mis_nodes,left_on='target',right_index=True,suffixes=('_source','_target'))

    edge_list_df.drop(['group_source','group_target','source','target'],axis=1,inplace=True)

    if float(nx.__version__)<2:
      return nx.from_pandas_dataframe(edge_list_df,'name_source','name_target')
    else:
      return nx.from_pandas_edgelist(edge_list_df, 'name_source', 'name_target')

def ex3_create_fair(p,thruth,dim):
    signal = []
    for t in thruth:
        if np.random.rand()<p:
            signal += [t]
        else:
            signal += [np.random.choice(list(set(range(dim))-set([t])))]
    return signal

def ex3_create_random_spammer(siglen,dim):
    return np.random.randint(dim,size=siglen).tolist()

def ex3_compute_accuracy(truth,signal):
    return (truth==signal).astype(int).sum()/len(truth)

def ex3_create_dataset(dim, signal_length):
    np.random.seed(42)

    truth = np.random.randint(dim,size=signal_length)

    workers        = []
    workers_labels = {}
    cnt            = 0
    # expert
    workers_labels['expert'] = []
    for i in range(10):
        workers += [ex3_create_fair(np.random.uniform(low=0.9,high=1.0),truth,dim)]
        workers_labels['expert'].append(cnt)
        cnt += 1

    # normal
    workers_labels['normal'] = []
    for i in range(10):
        workers += [ex3_create_fair(np.random.uniform(low=0.7,high=0.9),truth,dim)]
        workers_labels['normal'].append(cnt)
        cnt += 1

    # sloppy
    workers_labels['sloppy'] = []
    for i in range(20):
        workers += [ex3_create_fair(np.random.uniform(low=0.2,high=0.4),truth,dim)]
        workers_labels['sloppy'].append(cnt)
        cnt += 1

    # random
    workers_labels['random'] = []
    for i in range(50):
        workers += [ex3_create_random_spammer(signal_length,dim)]
        workers_labels['random'].append(cnt)
        cnt += 1

    workers = np.array(workers)
    return truth,workers,workers_labels
