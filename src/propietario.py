#Importamos las librerías necesarias para el trabajo
import whois

# Vemos las tecnologías usadas en la web
w = whois.whois('https://pccomponentes.com')
print(w)