import pydot


class PydotGraph:

    def __init__(self, node_defaults=None, edge_defaults=None):
        self.node_defaults = node_defaults
        self.edge_defaults = edge_defaults
        self.node_number = 0
        self.graph_number = 0
        self.antecedents = []
        self.root = None

    def configure_graph(self, graph: pydot.Graph):
        self.graph_number = self.graph_number + 1
        if graph.obj_dict["name"] == "":
            graph.obj_dict["name"] = pydot.quote_if_necessary(str(self.graph_number))
        else:
            graph.obj_dict["name"] = graph.obj_dict["name"] + "_" + pydot.quote_if_necessary(str(self.graph_number))
        if self.edge_defaults:
            graph.set_edge_defaults(**self.edge_defaults)
        if self.node_defaults:
            graph.set_node_defaults(**self.node_defaults)
        return graph

    def build(self, items: list = None, last_edge: pydot.Edge = None, last_node: pydot.Node = None):
        if self.root is None:
            self.root = graph = self.configure_graph(pydot.Dot())
        else:
            graph = self.configure_graph(pydot.Subgraph())
        for item in items:
            if isinstance(item, pydot.Graph):
                if not any(x is item for x in self.antecedents):
                    graph = self.configure_graph(item)
                else:
                    graph = item
            elif isinstance(item, pydot.Edge) and last_node:
                last_edge = item
            elif isinstance(item, pydot.Node):
                if not any(x is item for x in self.antecedents):
                    self.node_number = self.node_number + 1
                    if item.obj_dict["name"] == "":
                        item.obj_dict["name"] = pydot.quote_if_necessary(str(self.node_number))
                        graph.add_node(item)
                        self.antecedents.append(item)
                if last_edge and not any(x is last_edge for x in self.antecedents):
                    src = last_node.get_name()
                    dst = item.get_name()
                    points = (pydot.quote_if_necessary(src), pydot.quote_if_necessary(dst))
                    last_edge.obj_dict["points"] = points
                    graph.add_edge(last_edge)
                    self.antecedents.append(last_edge)
                last_node = item
            elif isinstance(item, list):
                sub = self.build(items=item, last_edge=last_edge, last_node=last_node)
                if not any(x is sub for x in self.antecedents):
                    graph.add_subgraph(sub)
                    self.antecedents.append(sub)
            else:
                raise
        return graph
