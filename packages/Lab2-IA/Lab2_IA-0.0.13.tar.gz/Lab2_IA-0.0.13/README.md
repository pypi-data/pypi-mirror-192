# UVG_IA_Lab2
Laboratorio 2 de Inteligencia Artificial

PyPI: https://pypi.org/project/Lab2-IA/
PR Aprobada (0.5 pts extras!): https://github.com/SantiagoTaracena01/cool-bayesian-networks/pull/2

## Instrucciones de empaquetamiento:
python setup.py sdist bdist_wheel

## Instrucciones de instalación:
pip install Lab2-IA==0.0.11

## Instrucciones de uso:
Para poder utilizar este paquete, se debe de hacer lo siguiente. Se debe de tener un archivo de texto de la siguiente manera
###### P(A) = 0.30
###### P(B) = 0.23
###### P(C|!A, !B) = 0.5
###### P(C|!A, B) = 0.10
###### P(C|A, !B) = 0.77
###### P(C|A, B) = 0.20

La estrucutra de debe der P(A) o P(C|A, B), donde después del "|", debe de estar la probabilidad, y para cada condicion añadida, se añade una coma y un espacio después para que se pueda leer. 

La estructura de las probabilidades condicionales, debe de ser que todas esten negadas al principio, y después empezar a negarlas de derecha a izquierda, hasta que todas sean las positivas.
