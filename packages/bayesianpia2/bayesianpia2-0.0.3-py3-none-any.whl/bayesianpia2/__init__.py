class BayesianNetwork:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.factors = {}

    def is_fully_described(self):
        for node in self.nodes:
            if node not in self.factors:
                return False
        return True

    def get_compact_representation(self):
        s = ""
        for node in self.nodes:
            s += f"{node}: "
            if node in self.factors:
                factor = self.factors[node]
                parents = self.edges[node]
                parent_names = [p for p in parents]
                parent_names.sort()
                s += f"{', '.join(parent_names)} | {node}\n"
                for k, v in factor.items():
                    parent_values = [str(k[i]) for i in range(len(parents))]
                    parent_values_str = ", ".join(parent_values)
                    s += f"    P({node}=True"
                    if len(parents) > 0:
                        s += f" | {' ,'.join([f'{parent_names[i]}={parent_values[i]}' for i in range(len(parents))])}"
                    s += f") = {v:.4f}, P({node}=False"
                    if len(parents) > 0:
                        s += f" | {' ,'.join([f'{parent_names[i]}={parent_values[i]}' for i in range(len(parents))])}"
                    s += f") = {1 - v:.4f}\n"
            else:
                parents = self.edges[node]
                parent_names = [p for p in parents]
                parent_names.sort()
                s += f"{', '.join(parent_names)} | {node}\n"
                s += f"    <probability table not defined>\n"
        return s

    def compute_factor(self, node, evidence={}):
        parents = self.edges[node]
        parent_names = [p for p in parents]
        parent_names.sort()
        parent_states = [(p, evidence.get(p, True)) for p in parent_names]
        factor = {}
        for i in range(2 ** len(parents)):
            parent_values = [bool((i // (2 ** j)) % 2) for j in range(len(parents))]
            parent_state = {parent_names[j]: parent_values[j] for j in range(len(parents))}
            parent_state.update(evidence)
            prob = self.compute_conditional_probability(node, parent_state)
            factor[tuple(parent_values)] = prob
        self.factors[node] = factor

    def compute_conditional_probability(self, node, parent_state):
        cpt = self.factors[node]
        parent_values = tuple([parent_state[p] for p in self.edges[node]])
        if parent_values in cpt:
            return cpt[parent_values]
        else:
            # if the parent configuration is not defined in the CPT,
            # we use Laplace smoothing to avoid zero probabilities
            alpha = 1
            num_states = len(cpt)
            num_true = sum([1 for k in cpt if k[-1]])
            num_false = num_states - num_true
            prob_true = (num_true + alpha) / (num_states + 2 * alpha)
            prob_false = (num_false + alpha) / (num_states + 2 * alpha)
            return prob_true if parent_state[self.edges[node][0]] else prob_false
