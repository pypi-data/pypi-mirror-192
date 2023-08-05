class Calculator:
    """ Class for performing basic arithmetic operations
    """
    def __init__(self):
        """ Construktor for Calculator
        
        """
        self.memory = 0
    def add(self, value:float)->float:
        """ Adds a value to the memory
        
        Args:
        value (float): The value to be added to the memory
        
        Returns:
        float: The updated value of the memory
        """
        self.memory += value
        print(self.memory)
        return self.memory

    def subtract(self, value:float)->float:
        """ Subtracts a value from the memory
        
        Args:
        value (float): The value to be subtracted from the memory
        
        Returns:
        float: The updated value of the memory
        """
        self.memory -= value
        print(self.memory)
        return self.memory

    def multiply(self, value:float)->float:
        """ Multiplies the memory by a value

        Args:
        value (float): The value to multiply the memory by

        Returns:
        float: The updated value of the memory
        """
        self.memory *= value
        print(self.memory)
        return self.memory

    def divide(self, value:float)->float:
        """ Divides the memory by a value
        
        Args:
        value (float): The value to divide the memory by
        
        Returns:
        float: The updated value of the memory
        """
        self.memory /= value
        print(self.memory)
        return self.memory

    def root(self, value:float)->float:
        """ Takes the nth root of the memory, where n is the value
        
        Args:
        value (float): The root to extract from the memory
        
        Returns:
        float: The updated value of the memory
        """
        self.memory =  self.memory ** (1/value)
        print(self.memory)
        return self.memory

    def reset(self):
        """ Resets the memory to 0
        
        Returns:
        None
        """
        self.memory = 0