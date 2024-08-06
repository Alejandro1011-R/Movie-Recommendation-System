import numpy as np

def find_neighbors(hybrid_matrix, user_id):
    """
    Encuentra los vecinos más cercanos (usuarios similares) para el usuario objetivo.

    Parameters
    ----------
    hybrid_matrix : DataFrame
        Un DataFrame que representa las preferencias de los usuarios por diferentes géneros.
    user_id : int
        El ID del usuario para el cual se quieren encontrar vecinos.

    Returns
    -------
    list of tuples
        Una lista de tuplas que representan los vecinos más cercanos y sus puntajes de similitud.
    """
    if user_id not in hybrid_matrix.index:
        raise ValueError("UserID not found in the hybrid matrix")

    num_rows = hybrid_matrix.shape[0] - 1
    k = min(20, int(num_rows * 0.15))  # Ajustar '20' según sea necesario
    if k < 1: k = 20

    similitudes = {}
    user_vector = hybrid_matrix.loc[user_id]
    for other_user in hybrid_matrix.index:
        if other_user == user_id:
            continue
        other_user_vector = hybrid_matrix.loc[other_user]
        if np.any(user_vector) and np.any(other_user_vector):
            sim = np.dot(user_vector, other_user_vector)
            norm_product = np.linalg.norm(user_vector) * np.linalg.norm(other_user_vector)
            if norm_product > 0:
                sim /= norm_product
            else:
                sim = 0
            similitudes[other_user] = sim

    sorted_neighbors = sorted(similitudes.items(), key=lambda x: x[1], reverse=True)
    return sorted_neighbors[:k]
