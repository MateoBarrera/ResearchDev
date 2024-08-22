import numpy as np


def generate_ahp_matrix(n):
    """
    Generate a random AHP criteria matrix of size n x n.

    Parameters:
    n (int): Number of criteria

    Returns:
    np.ndarray: AHP comparison matrix
    """
    # Initialize an n x n matrix with ones on the diagonal
    matrix = np.ones((n, n))

    # Fill the upper triangular matrix with random values (1 to 9)
    for i in range(n):
        for j in range(i + 1, n):
            # Generate a random value between 1 and 9 for the comparison
            value = np.random.randint(1, 10)
            matrix[i, j] = value
            matrix[j, i] = 1 / value

    return matrix


def main():
    # Input number of criteria
    num_criteria = int(input("Enter the number of criteria: "))

    # Generate AHP comparison matrix
    ahp_matrix = generate_ahp_matrix(num_criteria)

    # Print the AHP comparison matrix
    print("AHP Comparison Matrix:")
    print(ahp_matrix)


if __name__ == "__main__":
    main()
