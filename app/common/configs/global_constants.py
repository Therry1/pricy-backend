import enum

class EntityType(enum.Enum):
    WAREHOUSE = "WAREHOUSE"
    POS = "POS"           # Point de Vente
    SUPPLIER = "SUPPLIER" # Fournisseur
    PRODUCTION = "PRODUCTION" # Pour les transformations internes