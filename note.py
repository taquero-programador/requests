import requests

# marco un error en las depencias
pip3 install requests=2.28.1
# actualizar urllib3 y chardet
pip3 install package-name -U

r = requests.get('https://httpbin.org/get')
print(r.url)

# pasar un diccionario como argumentos
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get('https://httpbin.org/get', params=payload)
print(r.url)
# retorna la url y le añade la peticion despues del singo ?
# hay que tomas en cuenta que cualquier valor que sea None se añadira a la url

# para una lista de elementos como un valor
payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
r = requests.get('https://httpbin.org/get', params=payload)
print(r.url)

# contenido de la respuesta
r = requests.get('https://api.github.com/events')
print(r.text) # retorna un diccionario

# averiguar y cambiar la codificación
print(r.encoding) # retorna la codificacion usada
r.encoding = "ISO-8859-1"
print(r.encoding) # retorna la nueva codifiación

"""
los archivos HTML y XML tienen la capacidad de especificar su codificación en el cuerpo del documento.
para encontrar la code usar 'r.content' y despues 'r.encoding'. asi r.text usara la code correcta
"""

# contenido de respuesta binaria. acceder a la respuesta como bytes
print(r.content)

# crear una image a partir de los datos binarios devueltos
from PIL import Image
from io import BytesIO

i = Image.open(BytesIO(r.content))

# contenido de respuesta JSON
print(r.json())

# contenido de la respuesta sin procesar
r = requests('https://api.github.com/events', stream=True)
print(r.raw)
print(r.raw.read(10))

# guardar la lectura en un archivo de salida
with open("file.txt", "wb") as fd:
    for ch in r.iter_content(chunk_size=128):
        fd.write(ch)

# me marco error durante la salida, así que lo hago a mi manera
with open("file.txt", "w") as fd:
    for ch in r.text:
        fd.write(ch)

# apesar, .iter_content es la mejor forma de recuperar la informacion de la url

# encabezado personalizado. pasar una variable como argumento de tipo dict
url = 'https://api.github.com/some/endpoint'
headers = {'user-agent': 'my-app/0.0.1'}
r = requests.get(url, headers=headers)
print(r.url)
# los encabezados personalizados tiene menos prioridad, tampoco cambian
# el comportamiento de la solicitud, solo se pasan al final de la solicitud. los headers deben ser string

# solcitud POST más complicadas. enviar informacion codificada en formularios. el valor se manda en 'data'
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post("https://httpbin.org/post", data=payload)
print(r.text)
