# layout.py
from collections import namedtuple

# --- Layout class només per metadades i estils ---
class Layout:
    """
    Classe per definir com es representa l'arbre (metadades/estils) sense calcular coordenades.
    """
    def __init__(self, name, draw_tree=None, draw_node=None):
        self.name = name
        self.draw_tree = draw_tree  # dict o funció que retorna dict
        self.draw_node = draw_node  # funció per definir què mostra cada node

# --- Exemple simple de draw_node ---
def default_draw_node(node, collapsed):
    """Retorna només metadades d'un node"""
    if not collapsed:
        return [{'prop': 'dist', 'value': node.dist if hasattr(node,'dist') else 0},
                {'prop': 'support', 'value': getattr(node,'support',None)}]
    if getattr(node, 'is_leaf', False) or collapsed:
        return [{'prop': 'name', 'value': getattr(node, 'name', '')}]

BASIC_LAYOUT = Layout(name='basic', draw_node=default_draw_node)

# --- Label namedtuple (similar a Smartview) ---
Label = namedtuple('Label', 'code style node_type position column anchor fs_max')