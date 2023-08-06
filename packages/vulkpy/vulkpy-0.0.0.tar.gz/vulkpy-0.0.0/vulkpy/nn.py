from .vkarray import Array


class Module:
    def __init__(self):
        pass

    def __call__(self, x: Array):
        if len(x.shape) < 2:
            raise ValueError("Input must have at least 2-dimensions.")

        self._y = self.forward(x)
        return self._y

    def forward(self, x: Array):
        raise NotImplementedError


class ReLU(Module):
    def forward(self, x: Array):
        return x.max(0.0)

    def backward(self, y: Array):
        return y.sign()


class SoftMax(Module):
    def forward(self, x: Array):
        X = x - x.max(axis=1)
        X.exp(inplace=True)
        return X / X.sum(axis=1)

    def backward(self, y: Array):
        pass
