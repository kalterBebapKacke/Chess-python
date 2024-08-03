import torch

a = torch.rand(3, requires_grad=True)
y = a + 2
print(a)
print(y)

y.backward()
print(y)