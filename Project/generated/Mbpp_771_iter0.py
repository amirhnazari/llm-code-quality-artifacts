def check_expression(expression):
    # Initialize an empty stack to keep track of opening brackets
    stack = []
    
    # Dictionary to hold matching pairs of brackets
    bracket_pairs = {')': '(', '}': '{', ']': '['}
    
    # Iterate through each character in the expression
    for char in expression:
        # If the character is an opening bracket, push it onto the stack
        if char in "({[":
            stack.append(char)
        # If the character is a closing bracket
        elif char in ")}]":
            # If the stack is empty or the top of the stack doesn't match the corresponding opening bracket, return False
            if not stack or stack[-1] != bracket_pairs[char]:
                return False
            # Otherwise, pop the top element from the stack
            else:
                stack.pop()
    
    # If the stack is empty, all brackets were matched correctly; otherwise, return False
    return len(stack) == 0

# Test the function with the provided test case
assert check_expression("{()}[{}]") == True
