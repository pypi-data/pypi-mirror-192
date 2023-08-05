# Laboratorio 2
# Inteligencia Artificial
# Authors: YongBum Park 20117, Santiago Taracena 20017, Pedro Arriola 20188, Oscar López 20679

from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class Bayesian(object):
    def __init__(self):
        self.model = None
        self.infer = None

    def bayesian_network_construction(self, construct):
        # Create a Bayesian Network with the specified structure
        self.model = BayesianNetwork(construct)

    def asign_values(
        self, name, amount, probabilities, evidences=None, evidences_card=None
    ):
        # Define the conditional probability distribution for a node
        return TabularCPD(
            variable=name,
            variable_card=amount,
            values=probabilities,
            evidence=evidences,
            evidence_card=evidences_card,
        )

    def show_values(self, cpd):
        # Display the values of a conditional probability distribution
        print(cpd.values)

    def asign_to_model(self, values):
        # Add the conditional probability distributions to the model
        for value in values:
            self.model.add_cpds(value)

    def check_model(self):
        # Check if the model is valid
        return self.model.check_model()

    def check_nodes(self):
        # Display the nodes in the model
        print("Nodes\n", self.model.nodes())

    def check_edges(self):
        # Display the edges in the model
        print("Edges\n", self.model.edges())

    def show_model_construction(self, value):
        # Display the construction of the specified node in the model
        print("Model\n", self.model.get_cpds(value))

    def calculate_probability(self, variables, evidenced=None):
        # Calculate the probability of the specified variables given the evidence
        self.infer = VariableElimination(self.model)
        query = self.infer.query(variables=variables, evidence=evidenced)
        return query
