import graphviz as gv


class PathGraph(object):
    def __init__(self, input_curie, input_label):
        self.input_curie = input_curie
        self.input_label = input_label
        self.path_graph = gv.Digraph(name="Workflow II {} Implementation".format(self.input_label))
        self.single_node((self.input_curie, self.input_label))

    def single_node(self, node_tuple):
        '''
        input: tuple ('NodeID', 'NodeLabel')
        '''
        self.path_graph.node(PathGraph.conv_pref(node_tuple[0]), label=node_tuple[1])

    def load_nodes(self, node_list):
        '''
        input: list of tuples [('NodeID', 'NodeLabel')]
        '''
        for node in node_list:
            self.single_node(node)

    def single_edge(self, edge_tuple):
        '''
        input: tuple ('NodeID', 'NodeID')
        '''
        self.path_graph.edge(PathGraph.conv_pref(edge_tuple[0]), PathGraph.conv_pref(edge_tuple[1]))

    def load_edges(self, edge_list):
        '''
        input: list of tuples [('NodeID', 'NodeID')]
        '''
        for edge in edge_list:
            self.single_edge(edge)

    def module_inputs(self, input_gene_set, module_id):
        for input_gene in input_gene_set:
            self.single_edge((input_gene, module_id))

    def module_outputs(self, output_gene_set, module_id):
        for output_gene in output_gene_set:
            self.single_edge((module_id, output_gene))

    @staticmethod
    def conv_pref(prefix):
        return prefix.replace(':', '_')
