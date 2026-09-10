def get_Inv_Count(arr):
    # Initialize the inversion count to zero
    inv_count = 0
    
    # Iterate through each element in the array using enumerate for better readability
    for i, x in enumerate(arr):
        # Compare current element with all subsequent elements using list comprehension
        inv_count += sum(1 for y in arr[i + 1:] if x > y)
        
    return inv_count

# Test the function with the provided test case
assert get_Inv_Count([1, 20, 6, 4, 5]) == 5
