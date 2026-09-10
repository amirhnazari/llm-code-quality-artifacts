def check_expression(expression):
    """
    Check if the given expression is balanced.

    Args:
    expression (str): The expression to be checked.

    Returns:
    bool: True if the expression is balanced, False otherwise.
    """
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in expression:
        if char in mapping.values():
            stack.append(char)
        elif char in mapping:
            if not stack or mapping[char] != stack.pop():
                return False
    
    return not stack
