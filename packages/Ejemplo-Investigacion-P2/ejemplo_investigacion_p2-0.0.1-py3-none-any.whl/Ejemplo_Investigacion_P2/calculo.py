from Ejemplo_Investigacion_P2.constantes import PI
#Esta primera funcion lo que me permite es la suma de dos valores, que tambien se pueden modificar paara
#ser introducidos por el usuario.
def sum(num1:float, num2:float) -> float:
    return num1+num2
#Esta funcion me permite calcular el area del circulo, con solo ingresar el valor
#Es importante mencionar que se pueden agregar aun mas funciones a manera de herramientas segun la necesidad
# de los usuarios.
def area_circulo(radio:float) -> float:
    return radio*radio*PI