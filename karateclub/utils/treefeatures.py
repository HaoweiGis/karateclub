import hashlib
import networkx as nx

class WeisfeilerLehmanHashing(object):
    """
    Weisfeiler Lehman feature extractor class.
    """
    def __init__(self, graph, wl_iterations, attributed):
        """
        Initialization method which also executes feature extraction.
        :param graph: The NetworkX graph object.
        :param features: Feature hash table.
        :param iterations: Number of WL iterations.
        """
        self.wl_iterations = wl_iterations
        self.graph = graph
        self.attributed = attributed
        self._set_features()
        self._do_recursions()


    def _set_features(self):
        if self.attributed:
            self.features = nx.get_node_attributes(G, 'features')
        else:
            self.features = {node: self.graph.degree(node) for node in self.graph.nodes()}

    def _do_a_recursion(self):
        """
        The method does a single WL recursion.
        :return new_features: The hash table with extracted WL features.
        """
        self.extracted_features = [str(v) for k, v in self.features.items()]
        new_features = {}
        for node in self.graph.nodes():
            nebs = self.graph.neighbors(node)
            degs = [self.features[neb] for neb in nebs]
            features = [str(self.features[node])]+sorted([str(deg) for deg in degs])
            features = "_".join(features)
            hash_object = hashlib.md5(features.encode())
            hashing = hash_object.hexdigest()
            new_features[node] = hashing
        self.extracted_features = self.extracted_features + list(new_features.values())
        return new_features

    def _do_recursions(self):
        """
        The method does a series of WL recursions.
        """
        for _ in range(self.wl_iterations):
            self.features = self._do_a_recursion()
        
