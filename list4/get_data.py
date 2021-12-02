import itertools
import requests
import re
import pandas as pd
from unidecode import unidecode
from bs4 import BeautifulSoup
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import scipy

def download_and_save_data():
    URL = "http://prac.im.pwr.wroc.pl/~hugo/HSC/Publications.html"
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}
    session = requests.Session()
    cont = session.get(URL, headers=headers)
    with open('data.txt', 'w') as f:
        f.write(str(cont.content.decode('utf16')))


with open('data.txt', 'r') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")


def get_authors_of_research():
    parts_per_year = [ol for ol in soup.find_all("ol")[2:-6]]
    parts_per_year.reverse()
    authors = []
    in_bold = []
    for part in parts_per_year:
        whole_part = []
        for p in part.find_all("li"):
            whole_part += [a.get_text() for a in p.find_all("font") if all(['.' in a.get_text(), len(a.get_text().split(".")[0]) == 1])]
            pub = [a.get_text() for a in p.find_all("b")]
            in_bold += pub
            for auth in p.find_all("font"):
                if auth.get_text() in in_bold:
                    pub += [auth.get_text()]
            authors.append(list(set(pub)))

    return authors


def clean_text_regex(txt):
    pattern = "[^A-Za-z0-9-]"
    txt = re.sub(pattern, "9", txt)
    return txt


def clean_text(txt):
    txt = txt.replace(" ", "")
    txt = txt.capitalize()
    txt = unidecode(txt)
    return txt.split("-")[0] if "-" in txt else txt


def clean_authors_txt(authors):
    cleaned = []
    for paper in authors:
        cleaned.append(clean_text(author) for author in paper)
    return cleaned


def get_authors_lists():
    list_of_authors = []
    authors = get_authors_of_research()
    cleaned_authors = clean_authors_txt(authors)
    for aut in cleaned_authors:
        mini_list = []
        [mini_list.append(j) for j in aut]
        list_of_authors.append(mini_list)
    return list(filter(None, list_of_authors))

#authors_list = get_authors_lists()

def get_authors_size():
    authors_list = get_authors_lists()
    count = pd.Series(authors_list).explode().value_counts()
    return dict(count)
authors_sizes = get_authors_size()

def get_authors_once():
    authors_list = get_authors_lists()
    author1 = []
    for i in authors_list:
        if all([len(i) == 1]):
            author1.append(i)
    return author1

def get_authors_pairs():
    authors_list = get_authors_lists()
    author_pairs = [i for i in authors_list if len(i) == 2]
    authors_above_2 = [j for j in authors_list if len(j) > 2]
    pairs = []
    for group in authors_above_2:
        combinations = list(itertools.combinations(group, 2))
        for pair in combinations:
            pairs.append(list(pair))
    author1 = get_authors_once()
    author_pairs = author_pairs + pairs # + author1
    return dict(Counter(tuple(sorted(tup)) for tup in author_pairs))

authors_dict = get_authors_pairs()


G = nx.Graph()
sizes = []
for n in authors_sizes.items():
    G.add_node(n[0])
    sizes.append(n[1]*3)

for k, v in authors_dict.items():
    G.add_edge(k[0], k[1], weight=v)


# from pylab import rcParams
# rcParams['figure.figsize'] = 11, 7
# pos = nx.spring_layout(G, k=2, iterations=100, scale=2)
# nx.draw_networkx(G, pos, with_labels=True, node_size=sizes, font_size=6,
#                  node_color='lightblue', edge_color='grey', width=0.5)
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=6,
#                              label_pos=0.5)

popular = G.degree
bridge = list(nx.bridges(G))
avg_conn = nx.average_node_connectivity(G)
isolates = list(nx.isolates(G))
closeness = nx.closeness_centrality(G)

# x, y = [], []
# for name, clos in closeness.items():
#     x.append(name)
#     y.append(clos)
# plt.plot(x, y, 'o')

# clusters = nx.clustering(G)


from matplotlib.cm import ScalarMappable
import networkx as nx

# g = nx.erdos_renyi_graph(50, 0.1, seed=None, directed=False)
# gc = g.subgraph(max(nx.connected_components(g)))
# lcc = nx.clustering(gc)

lcc = nx.clustering(G)

cmap = plt.get_cmap('autumn')
norm = plt.Normalize(0, max(lcc.values()))
node_colors = [cmap(norm(lcc[node])) for node in G.nodes]

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 4))
pos = nx.spring_layout(G, k=2, iterations=100, scale=2)
nx.draw_networkx(G, pos, with_labels=True, node_size=sizes, font_size=6,
                 node_color=node_colors, edge_color='grey', width=0.5, ax=ax1)
# nx.draw_spring(G, node_color=node_colors, with_labels=True, ax=ax1)
fig.colorbar(ScalarMappable(cmap=cmap, norm=norm), label='Clustering', shrink=0.95, ax=ax1)

ax2.hist(lcc.values(), bins=10)
ax2.set_xlabel('Clustering')
ax2.set_ylabel('Frequency')
plt.tight_layout()