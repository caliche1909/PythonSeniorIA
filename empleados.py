from abc import ABC, abstractmethod

class Trabajable(ABC):
    @abstractmethod
    def trabajar(self):
        pass


class Empleado(ABC):
    def __init__(self, nombre, salario_base):
        self.nombre = nombre
        self.salario_base = salario_base
    
    @abstractmethod
    def calcular_salario(self):
        pass
    
    def mostrar_info(self):
        return f"Empleado: {self.nombre}, Salario Base: ${self.salario_base:,}"
    
class Gerente(Empleado, Trabajable):
    def __init__(self, nombre, salario_base, bono):
        super().__init__(nombre, salario_base)
        self.bono = bono
    
    def calcular_salario(self):
        return self.salario_base + self.bono
    
    def trabajar(self):
        return f"{self.nombre} está supervisando al equipo y tomando decisiones estratégicas."


class Desarrollador(Empleado, Trabajable):
    def __init__(self, nombre, salario_base, lenguaje ):
        super().__init__(nombre, salario_base)
        self.lenguaje = lenguaje
      
    def calcular_salario(self):
        return self.salario_base
    
    def trabajar(self):
        return f"{self.nombre} está programando en {self.lenguaje}."
    

empleados = [
    Gerente("Ana", 4000, 1000),
    Desarrollador("Luis", 3000, "Python"),
]


for empleado in empleados:
    print(empleado.mostrar_info())
    print(f"Salario Total: ${empleado.calcular_salario():,}")
    print(empleado.trabajar())
    print("-" * 40)
    if isinstance(empleado, Trabajable):
        print(empleado.trabajar())
        print("-" * 40)