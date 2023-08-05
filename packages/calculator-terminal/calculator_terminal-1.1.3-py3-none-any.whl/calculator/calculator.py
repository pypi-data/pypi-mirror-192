from .extensions.operaciones import Operacion; from extensions.operaciones import Suma, Resta, Multiplicacion, Division
from .extensions.errors.error_handler import *
from typing import Union, Optional, Tuple, Dict
def Calcular(interactive:bool = False, operacion:Operacion = Suma, *, num1:Optional[Union[int, float]] = None, num2:Optional[Union[int, float]] = None) -> None:
    """
    Ejecuta una suma.

    Atributos
    -----------
    interactive: :class:`bool`
        Si la calculadora debería ser interactiva (respuesta en la terminal).
        En caso de ser :bool:`True`, los parámetros :param:`num1` y :param:`num2` no deben de ser especificados.
        En caso de ser :bool:`False`, los parámetro :param:`num1` y :param:`num2` deben de ser especificados.

    operacion: :class:`Operacion`
        La operación a realizar.

    num1: :Optional::Union:`int | float`
        El primer número a ser calculado.
        Si este parámetro es especificiado mientras :param:`interactive` es :bool:`True` saltará un error.

    num2: :Optional::Union:`int | float`
        El segundo número a ser calculado.
        Si este parámetro es especificado mientras :param:`interactive` es :bool:`True` saltará un error.

    Excepciones
    -----------
    IsInteractive
        Cuando se ha proporcionado los parámetro :param:`num1` y :param:`num2` mientras :param:`interactive` era :bool:`True`

    MissingParameter
        Cuando no se ha proporcionado uno o los dos de los parámetro :param:`num1` y :param:`num2` mientras :param:`interactive` era :bool:`False`
    """

    if interactive == True:
        if num1 != None or num2 != None:
            if num1 != None and num2 != None:
                raise IsInteractive(None, ("num1, num2"))

            elif num1 != None and num2 == None:
                raise IsInteractive(None, "num1")

            elif num1 == None and num2 != None:
                raise IsInteractive(None, "num2")

        if operacion not in [Suma, Resta, Multiplicacion, Division]:
            raise InvalidOperation(None, "operacion")

        if operacion == Suma:
            num1 = int(input("¿Cuál sería el primer número?\n"))
            num2 = int(input("¿Cuál sería el segundo número?\n"))

            oper = Suma.__name__

            resultado: int = num1+num2

        if operacion == Resta:
            num1 = int(input("¿Cuál sería el primer número?\n"))
            num2 = int(input("¿Cuál sería el segundo número?\n"))

            oper = Resta.__name__

            resultado: int = num1-num2

        if operacion == Multiplicacion:
            num1 = int(input("¿Cuál sería el primer número?\n"))
            num2 = int(input("¿Cuál sería el segundo número?\n"))

            oper = Multiplicacion.__name__

            resultado: int = num1*num2

        if operacion == Division:
            num1 = int(input("¿Cuál sería el primer número?\n"))
            num2 = int(input("¿Cuál sería el segundo número?\n"))

            if num2 == 0:
                raise ZeroDivision(None, "num2")

            oper = Division.__name__

            resultado: int = num1/num2

        print("La {} de".format(oper.lower()), str(num1) ,"y", str(num2) ,"es" + "\n" + str(resultado))
        

    if interactive == False:
        if num1 == None or num2 == None:
            if num1 == None and num2 == None:
                raise MissingParameter(None, ("num1, num2"))

            elif num1 == None and num2 != None:
                raise MissingParameter(None, "num1")

            elif num1 != None and num2 == None:
                raise MissingParameter(None, "num2")


        if operacion not in [Suma, Resta, Multiplicacion, Division]:
            raise InvalidOperation(None, "operacion")

        num1 = int(num1)
        num2 = int(num2)

        if operacion == Suma:
            resultado: int = num1+num2

        if operacion == Resta:
            resultado: int = num1-num2

        if operacion == Multiplicacion:
            resultado: int = num1*num2

        if operacion == Division:
            if num2 == 0:
                raise ZeroDivision(None, "num2")

            resultado: int = num1/num2

        return resultado