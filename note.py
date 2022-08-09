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
# retorna la url y le añade la peticion despues del singo ? https://httpbin.org/get?name=javier
# hay que tomas en cuenta que cualquier valor que sea None se añadira a la url

# las demás peticiones HTTP
# post usa data
url = "https://httpbin.org/post"
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post(url, data=payload)
print(r.text) # https://httpbin.org/post?key1=value1&key2=value2 retorna un texto completo
# get usa params
url = "https://httpbin.org/get"
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.get(url, params=payload)
print(r.url) # https://httpbin.org/get?key1=value1&key2=value2 retorna url (se abre en navegador)
# pust usa data
url = "https://httpbin.org/put"
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.put(url, data=payload)
print(r.text) # retorna todo el texto
# las demás
r = requests.delete('https://httpbin.org/delete')

r = requests.head('https://httpbin.org/get')

r = requests.options('https://httpbin.org/get')

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

# pasa pasar mutiples valores usar una dict con listas o una lista de tuplas
payload_tuples = [('key1','value1'), ('key2', 'value2')]
r = requests.post('https://httpbin.org/post', data=payload_tuples)
payload_dict = {'key1': 'value1', 'key2': 'value2'}
r2 = requests('https://httpbin.org/post', data=payload_dict)
print(r.text)
# comparar tuple and dict
print(r.text == r2.text) # debe retornar True

# si se pasa como un string en lugar de un dict, los datos se publicaran directamente

# la api de github acepta POST/PATCH en json
import json

url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
r = requests.post(url, data=json.dumps(payload))
print(r.text)

# el código anterior no agrega el content al encabezado, si no se deasea decodificar el dict, no usar dumps
url = 'https://api.github.com/some/endpoint'
payload = {'some': 'data'}
r = requests.post(url, data=payload)
print(r.text)

# POST un archivo codificado en varias partes. la solicitudes simplifican la carga de archivos codificados en varias partes
url = 'https://httpbin.org/post'
file = {'file': open('file.xlsx', 'rb')}
r = requests.post(url, files=files)
print(r.text)
# puede establecer el nombre de archivo, el tipo de contenido y los encabezados de forma explicita
url = 'https://httpbin.org/post'
files = {'file': ('file.xlsx', open('file.xlsx', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}
r = reques.post(url, files=files)
print(r.text)

# enviar cadenas que se reciban como archivos
url = 'https://httpbin.org/post'
files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
r = requests.post(url, files=files)
print(r.text)

# codigós de estado de respuesta. usar .status_code
url = requests.get('https://httpbin.org/get')
print(url.status_code) # retorna el estado en numero
# integra la busqueda de estado
print(r.status_code == requests.codes_ok) # retorna True or False

# encabezados de respuesta usando un dict para acceder a los valores
print(r.headers)
# or
print(r.headers['Content-Type']) # mayusculas o minus

# cookies. se puede acceder a algunas cookies en las respuestas
url = 'http://example.com/some/cookie/setting/url'
r = requests.get(url)
print(r.cookies['example_cookie_name'])
# enviar las propias cookies
url = 'https://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
print(r.text) # retorna un dict


