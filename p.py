def solution(l, k):
    c = l
    while c:
        if c.next and c.next.value == k:
            c.next = c.next.next
        else:
            c = c.next
    return l.next if l and l.value == k else l

# Define a simple Node class for the linked list
class Node:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next

# Create a sample linked list
# Here we create a linked list with values 1, 2, 3, 4, 5
# The last node has a value of 3, which we will remove later
n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n5 = Node(5)
n1.next = n2
n2.next = n3
n3.next = n4
n4.next = n5

# Call the solution function with the sample linked list and value k = 3
result = solution(n1, 3)

# Print the resulting linked list after calling the solution function
# This should print: 1, 2, 4, 5
while result:
    print(result.value)
    result = result.next
