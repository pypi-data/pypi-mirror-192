from sys import argv
import numpy as np
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

class redBayesiana:

    def __init__(self, edges):
        """
            Parámetros
            ----------
                - Edges: Relaciones de dependencia. (Lista de tuplas).

            Los nodos se definen a partir de las relaciones de dependencia.
        """
        self.model = BayesianNetwork(edges)

    def cdp(self, variable, variable_card, values, evidence=None, evidence_card=None):
        """
            Función para agregar las distribuciones de probabilidad condicional de las variables.
            Parámetros
            ----------
                - variable: La variable cuyo CPD está definido. (int/string)
                - variable_card: Números de estados o cardinalidad. (int)
                - values: Probabilidad asignada.
                - evidence: Variables evidencia (list)
                - evidence_card: Número de variables de evidencia o cardinalidad (int)

            Returns
            -------
            CDF agregado.
        """
        cpd = TabularCPD(
                            variable=variable,
                            variable_card=variable_card,
                            values=values,
                            evidence=evidence,
                            evidence_card=evidence_card
                        )
        return self.model.add_cpds(cpd)

    def correcta(self):
        """
            Función para verificar que los nodos y los CDP estén definidos correctamente.
        """
        return self.model.check_model()

    def completamenteDescrita(self):
        """
            Función para conocer si la Red Bayesiana está o no completamente descrita.

            Returns
            -------
            Booleano para indicar si está completamente descrita o no.
        """

        cpds = self.model.get_cpds()
        if not cpds:
            # Un nodo no tiene CDP asociado
            return False
        else:
            for cpd in cpds:
                if np.isnan(cpd.values).any():
                    # El nodo cuenta con un CDP pero no describe todas las probabilidades
                    return False
            else:
                return True

    def compact(self):
        """
            Función para mostrar las distribuciones de probabilidad condicional de una forma más intuitiva y compacta.

            Returns
            -------
            String de la Red Bayesiana compactada.
        """
        output = f"Nodes: {', '.join(self.model.nodes())}\n"
        for node in self.model.nodes():
            cpd = self.model.get_cpds(node)
            if cpd:
                output += f"\nCPD of {node}:"
                output += f"\n{cpd}\n"
        return output
    
    
    def diccionario(self):
        """
            Función para obtener la Red Bayesiana como un diccionario.

            Returns
            --------
            Diccionario con información de la Red Bayesiana.
        """
        cpds = {}
        variables = list(self.model.nodes())
        for node in variables:
            cpd = self.model.get_cpds(node)
            if cpd:
                cpds[node] = {
                    "Probabilidades": cpd.values,
                    "Variables de evidencia": list(cpd.variables),
                    "No. Variables de evidencia": list(cpd.cardinality)
                }
        return cpds

    def inferencia(self, variable, evidence):
        """
            Función para calcular una inferencia.

            Parámetros
            -----------
                - variable: Variable sobre la que se hará la inferencia (list)
                - evidence: Variables observadas (dict)

            Returns
            --------
            Inferencia.
        """
        inf = VariableElimination(self.model)
        res = inf.query(variable, evidence=evidence)
        return res


def main (edges):
    redBayesiana(edges)

if __name__ == "__main__":
    main()