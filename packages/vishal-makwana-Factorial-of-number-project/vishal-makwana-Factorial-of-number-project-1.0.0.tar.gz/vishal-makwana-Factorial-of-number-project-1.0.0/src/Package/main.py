"factorial function"
def factorial(number):
    """
    function for the calculating the factorial of a number.
    Args:
        number (int): int number 

    Returns:
        (int) output factorial number.
    """    
    if number == 0 or number == 1:
        return 1
    else:
        return number*factorial(number-1)