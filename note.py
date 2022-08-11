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
# las cookies devuelven un RequestsCookieJar(), que actua como un diccionarion para uso multiple en dominios o rutas
jar = requests.cookies.RequestsCookieJar()
jar.set('tasty_cookie', 'yum', domain='httpbin.org', path='/cookies')
jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')
url = 'https://httpbin.org/cookies'
r = requests.get(url, cookies=jar)
r.text
# redirección e historial. usar la propiedad history para rastrear la redirección y completar la solicitud
# github redirije las solicitudes HTTP a HTTPS
r = requests.get('http://github.com/')
print(r.url)
print(r.status_code)
print(r.historial)
# si utiliza algun tipo de requests se puede desactivar con con el parametro allow_redirects
r = requests.get('http://github.com/', allow_redirects=False)
print(r.status_code)
print(r.history)
# lo que hace es deactivar la redireccion y retorna una url de HTTP
# al estar en head se puede habilitar
r = requests.head('http://github.com/', allow_redirects=False)
print(r.url)
print(r.status_code)
print(history)
# timesouts. puede pasar una argumento timeoutque le indique a la solicitus esperar un tiempo determinado
# en código de producción debe de implementarse
r = requests.get('http://github.com/', timeout=0.001)
print(r)
# requests advanced
"""
objetos de sesión
Session perimte persistir ciertos datos, tambien persiste los datos de as cookies.
un metodo session tiene todas las peticiones principales de API. se apoya de urllib3
"""
# persistir alguna cookies de la solicitud
s = requests.Session()
s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
r = s.get('https://httpbin.org/cookies')
print(r.text)
# tambien se puede usar para pasar datos predeterminados
s = requests.Session()
s.auth = ('user', 'pass')
s.headers.update({'x-test': 'true'})
s.get('https://httpbin.org/headers', headers={'x-test': 'true'})
# cualquier diccionario que se pase como metodo se fucionara con el valor de nivel session.

# los parametros de nivel metodo no persisten, por lo que se enviara en la primera solicitud pero no en la seguna
s = requests.Session()
r = s.get('https://httpbin.org/cookies', cookies={'from-my': 'browser'})
print(r.text)

r = s.get('https://httpbin.org/cookies')
print(r.text)
# para añadir manualmente cookies a la sesión usar la funcion Session.cookies

# la sesiones tambien se pueden usar como adminstradores de contexto
with requests.Session() as s:
    s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
# con eso se asegura de termina el proceso cuando salga del bucle
"""
objetos de solicitus y respuesta
cuando se llama a Request.get(), primero construye un requests que sera enviado
para solicita o consultar un recurso. en segundo lugar genera un Response que
se obtiene de la respuesta del servidor
"""
# solicitud para obtener informacion de wikipedia
url = 'https://en.wikipedia.org/wiki/Monty_Python'
r = request.get(url)
# acceder a los encabezados
print(r.headers)
# solicitud del encabezado
print(r.request.headers)
# solicitudes preparadas. trabajar directamente con el cuerpo o encabezado
from requests import Request, Session

s = Session()
req = Request('POST', url, data=data, headers=headers)
prepped = req.prepare()

prepped.body = 'this body'
del prepped.headers['Content-Type']
resp = s.send(prepped,
    stream=stream,
    verify=verfy,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)
print(resp.status_code)
#
from requests import Request, Session

s = Session()
req = Request('GET',  url, data=data, headers=headers)

prepped = s.prepare_request(req)

# do something with prepped.body
prepped.body = 'Seriously, send exactly these bytes.'

# do something with prepped.headers
prepped.headers['Keep-Dead'] = 'parrot'

resp = s.send(prepped,
    stream=stream,
    verify=verify,
    proxies=proxies,
    cert=cert,
    timeout=timeout
)
#
from requests import Request, Session

s = Session()
req = Request('GET', url)

prepped = s.prepare_request(req)

# Merge environment settings into session
settings = s.merge_environment_settings(prepped.url, {}, None, None, None)
resp = s.send(prepped, **settings)

print(resp.status_code)
# verificacion de certificados SSL. por defecto esta deshabiliatado
import requests
url = 'https://requestb.in'
r = Request.get(url)
print(r.text)
# retorna error y status code 200 al no poder verificar el certificado
# pasar verify con la ruta de archivo
Request.get(url, verify='path/cert')
# de manera persistente
s = Request.Session()
s.verify = 'path/cert'
# ingorar la verifiacion de SSL
url = 'https://requestb.in'
r = requests.get('https://requestb.in', verify=False)
print(r.text)
# deshabilitar la verificacion puede presentar serios problemas de vulnerabilidad

# certificados del lado del cliente. usar un certificado local de clave privada y certificado.
Request.get(url, cert=('path/cert.cert', 'path/cert.key'))
# persistente
s = requests.Session()
s.cert = 'path/file.cert'

# certificados CA. flujo de trabajo del contenido, de manera automatica descarga
# el cuerpo de la respuesta, esto puede ser anulado, con el parametro stream
url = 'https://github.com/psf/requests/tarball/main'
r = Request.get(url, stream=True)
print(r.text)
# esto mantiene la conexion abierta y no permite condicionar la recuperación del contenid
with open('massive-body', 'rb') as f:
    requests.post('http://some.url/streamed', data=f)
# solicitudes codificadas de fragmentos. permite fragmentos de solicitudes entrantes y salientes
# pasar un generador sin longitud
def gen():
    yield 'hi'
    yield 'there'

requests.post(url, data=gen())

# POST multiples archivos codificados en varias partes.
# enviar varios en una sola colicitud. cargar varias imagenes en un formulario
<input type="file" name="images" multiple="true" required="true"/>

# manera explicita
url = 'https://httpbin.org/post'
multiple_files = [

    ('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),

    ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]

r = requests.post(url, files=multiple_files)
print(r.text)
# usando un diccionario, es más corto
files = {'file1': open('foo.png', 'rb'), 'file2': open('bar.png', 'rb')}
r = Request.post(url, files=files)
print(r.text)
# en ambos casos debe retornar un parte que dice multipart/form-data

# hooks de eventos. manipular parte de proceso o el manejo de eventos
# reponse: respuesta generada a partir de una solicitud pasando un diccionario
hooks = {'response': print_url}
# callback_function recibe una porcion de datos como primer argumento
def print_url(r, *args, **kwargs):
    print(r.url)

# se deben controlar las excepciones
# si la funcion devuelve un valor, es porque reemplazara los datos que se pasaron
def record_hook(r, *args, **kwargs):
    r.hook_called = True
    return r
# imprimir argumentos en tiempo de solicitud
url = 'https://httpbin.org/'
r = requests.get(url, hooks={'response': print_url})
print(r)
# añadir multiples hooks
r = requests.get(url, hooks={'reponse': [print_url, record_called]})
print(r.hook_called)
# agragar hooks en Session()
s = Request.Session()
s.hooks['response'].append(print_url)
r = s.get('https://httpbin.org/')
print(r)

"""
autenticación personalizada
un argumento auth se podra modificar antes de ser enviado.

ejemplo donde un servicio web solo responde si 'X-Pizza' esta en el encabezado.
"""
from Request.auth import AuthBase

class PizzaAuth(AuthBase):
    def __init__(self, username):
        self.username = username

    def __call__(self, r):
        r.headers['X-Pizza'] = self.username
        return r
# lanzar la solicitud usando PizzaAuth
url = 'http://pizzabin.org/admin'
r = Request.get(url, auth=PizzaAuth('kenneth'))
print(r)

# solicitudes de transmision. con Response.iter_line se puede iterar sobre una api de twitter
# usar stream=True sobre el request y usar .iter_lines()
import json
import requests

url = 'https://httpbin.org/stream/20'
r = Request.get(url, stream=True)

for line in r.iter_lines():
    if line:
        decode_line = line.code('utf-8')
        print(json.loads(decode_line))

# proporcionar una codificación en caso de que el servidor no la de
url = 'https://httpbin.org/stream/20'
r = Request.get(url, stream=True)

if r.encoding is None:
    r.encoding = 'utf-8'

for line in r.iter_lines():
    if line:
        print(json.loads(line))

# proxies. crear un diccionarion y pasarlo como argumento de proxies dentro del requests
import requests

proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080'
}

r = requests.get('example.com', proxies=proxies)
print(r)
# configurarlo para toda la sesión de manera persistente
se = Request.Session()
se.proxies.update(proxies)
r = se.get(url)
print(r)
# socks. requiere libreria de terceros
python3 -m pip3 install requests[socks]
# usar proxy socks
proxies = {
    'http': 'socks5://user:pass@host:port',
    'https': 'socks5://user_pass@host:port'
}
# requests proporciona casi la gama completa de respuestas HTTP.
# HTTP GET
import requests

url = 'https://api.github.com/repos/psf/requests/git/commits/a050faf084662f3a352dd1a941f2c7c9f886d4ad'
r = requests.get(url)
# confirmar la respues
if r.status_code = requests.codes.ok:
    print(r.headers['Content-type'])
# de ser correcto es status_code retornara el encabezado
# github retorna un JSON, se puede manejar con r.json()
commit = r.json()
print(commit.keys()) # retorna las llaves
print(commit['committer']) # retorna el valor de commiter
print(commit['message'])
# usar el metodo .options para ver los tipos HTTP compatibles con la URL
verbs = requests.options(r.url)
print(verbs.status_code)
# no retorna los metodos pues gh no implmenta options
print(verbs.headers['allow']) # retorna los metodos disponibles
# probrar 482 git
import requests
import json
url = 'https://api.github.com/repos/psf/requests/issues/482'
r = requests.get(url)
print(r.status_code)
issue = json.loader(r.text)
print(issue['title'])
print(issue['comments'])
# en comments tenemos 3 comentarios
r = requests.get(url + '/comments')
print(r.status_code)
comments = r.json()
print(comments[0].keys())
print(comments[2]['body'])
print(comments[2]['user']['login'])
# crear un post con mediante la API
body = json.dumps({u"body": u"Sounds great! I'll get right on it!"})
url = u"https://api.github.com/repos/psf/requests/issues/482/comments"
r = requests.post(url, data=body)
print(r.status_code)
# retona un error 404, tal vez se requiera autenticación
from Request.auth import HTTPBasicAuth

auth = HTTPBasicAuth('fake@example.com', 'no_pass')
r = requests.post(url, data=body, auth=auth)
print(r.status_code)
content = r.json()
print(content['body']) # retorna la cadena de post
# actualizar el post con PATCH
print(content[u"id"])
body = json.dumps({u"body": u"Sounds great! I'll get right on it once I feed my cat."})
url = u"https://api.github.com/repos/psf/requests/issues/comments/5804413"
r = requests.patch(url, data=body, auth=auth)
print(r.status_code) # debe retornar 200, exitoso
# eliminar
r = requests.delete(url=url, auth=auth)
print(r.status_code) # 204
print(r.headers['status']) # '204 No Content'
r = requests.head(url=url, auth=auth)
print(r.headers)
'x-ratelimit-remaining': '4995'
'x-ratelimit-limit': '5000'

# Autenticacion
# autenticacion básica. hacer solicitudes con HTTPBasicAuth
from requests.auth import HTTPBasicAuth

basic = HTTPBasicAuth('user', 'pass')
url = 'https://httpbin.org/basic-auth/user/pass'
r = requests.get(url, auth=basic)
print(r.text) # retorna un dict con los valores de auth
print(r.status_code) # retorna 200, exito
# pasar directo como argumento de tipo tupla
requests.get(url, auth=('user', 'pass'))
"""
autenticación netrc
el archivo netrc anula los encabezados de autenticación HTTP sin establecer el formato headers=
"""
# autenticación implicita. autenticacion digest
import requests
from requests.auth import HTTPDigestAuth

url = 'https://httpbin.org/digest-auth/auth/user/pass'
r = requests.get(url, auth=HTTPDigestAuth('user', 'pass'))
print(r) # <Response [401]>
print(r.status_code)
# autenticacion OAuth1. una forma común de auth en APIS es OAuth
import requests
from requests.oauthlib import OAuth1

url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1('YOUR_APP_KEY', 'YOUR_APP_SECRET',
 'USER_OAUTH_TOKEN', 'USER_OAUTH_TOKEN_SECRET')
r = requests.get(url, auth=auth)
print(r) # reponse 200

# ------------------------------------------------------
# realpython api rest

# acceder a la info de un usuario en github
url = 'https://api.github.com/users/'
"""
metodos HTTP
GET: recupera recursos existentes
POST: crear un nuevo recurso
PUT: actualiza un recurso existente
PATCH: actualiza parcialmente un recurso existentes
DELETE: elimina un recurso

Codigós de estado
200: OK - accion solicitada exitosa
201: CREATED - se creó un nuevo recurso
202: Accepted - solicitud exitosa, sin peticiones
204: No Content - exitosa, respuesta sin contenido
400: Bad Request - solicitud mal formulada
401: Unauthorized - cliente no autorizado para la accion solicitada
404: Not Found - no se encontro el recurso
415: Unsupported Media Type - formato de datos con compatible con el servidor
422: Unprocessable Entity - datos de solicitud en formato correcto, pero con datos invalido o faltantes
500: Internal Server Error - servidor arrojo un error al procesar la solicitud

Rango de códigos
2xx: operación exitosa
3xx: redirección
4xx: error del cliente
5xx: error del servidor
"""
# endpoints. url publicas para acceder a los recursos de un servicio web
"""
Ejemplo de endpoints
GET: /customers - obtiene una lista de clientes
GET: /customers/<customer_id> - obtiene un solo cliente
POST: /customers - crea un nuevo cliente
PUT: /customers/<customer_id> - actualiza un cliente
PATCH - /customers/<customer_id> - actualiza parcialmente un cliente
DELETE: /customers/customer_id<> - elimina un cliente

cada uno de los enpoints realiza una acción diferente.

en los puntos finales <customer_id> esto significa que tiene que pasar un valor a trabajar.

esto es solo un ejemplo en algunos casos pueden ser cientos de endpoints
"""

# GET. este metodo permite recuperar los recuros de la API, es de solo lectura y no se debe usar para modificar
# https://jsonplaceholder.typicode.com/ proporciona endpoints falsos para pruebas

import requests

url = "https://jsonplaceholder.typicode.com/todos/1"
r = requests.get(url)
print(r.json())
print(r.status_code)
print(r.headers['content-type'])

# POST. enviar informacion al post
url = "https://jsonplaceholder.typicode.com/todos"
todo = {
    'userId': 1,
    'title': 'Buy milk',
    'completed': False
}
r = requests.post(url, data=todo)
print(r.json()) # retorna una sola linea en dict
print(r.text) # retorna un dict de varias linea k:v
# si no se pasa el argumento json se tiene que especificar 'Content-type'
# si no se importa json
import requests
import json

url = "https://jsonplaceholder.typicode.com/todos"
todo = {
    'userId': 1,
    'title': 'Buy milk',
    'completed': False
}
headers = {'Content-Tyep': 'application/json'}
r = requests.post(url, data=json.dumps(todo), headers=headers)
print(r.text)
print(r.status_code)
# PUT. actualizar un elemento
import requests

api_url = "https://jsonplaceholder.typicode.com/todos/10"
r = requests.get(url, )
print(r.json)
# pasar el metodo PUTS
todo = {
    'userId': 1,
    'title': 'Wash car',
    'completed': True
}
r = requests.put(api_url, json=todo)
print(r.json())
print(r.status_code)
# primero recuera un recurso de la api y con put actualiza ese recurso
# PATCH. para modificar un recurso pero no reemplaza completamente el recurso, solo actualiza
# los valores establecido en el json
todo = {'title': 'Mow lawn'}
r = requests.patch(url, json=todo)
print(r.json())
# ejecuta get, crear un nuevo recurso y despues actualiza parcialmente el recurso

# delete. eliminar por completo un recurso
import requests

api_url = "https://jsonplaceholder.typicode.com/todos/10"
r = requests.delete(api_url)
print(r.json())
print(r.status_code)

"""
REST y python: creación de API's
identificar recursos.
el primer paso para crear API's es identificar los recursos que administraran la API.
a medida que se identifiquen los recursos, crear una lista de sustantivo que describan los
diferente datos que los usarios pueden identificar.

considerar cualquier recurso anidado. establecer jerarquias de los recursos ayuda
a la definicion de los endpoint
"""

"""
definir puntos finales
una vez que se indentifiquen los recursos es momento para definir los endpoints
definicion de algunos endpoints de transaction

GET: /transactions - obtiene una lista de transacciones
GET: /transactions/<transaction_id> - obtiene una sola transacción
POST: /transactions - crea una nueva transaccón
PUS: /transactions/<transaction_id> - actualiza una sola transacción
PATCH: /transactions/<transaction_id> - actualiza de manera parcial un transacción
DELETE: /transactions/<transaction_id> - elimina una transacción

recursos anidados de endpoint.
GET: /events/<event_id>/guests - consigue una lista de invitados
GET: /events/<event_id>/guests/<guest_id> - obtiene un solo invitado
POST: /events/<event_id>/guests - crea un nuevo invitado
PUT: /events/<event_id>/guests/<guest_id> - actualiza un invitado
PATCH: /events/<event_id>/guests/<guest_id> - actualiza de manera parcial un recurso
DELETE: /events/<event_id>/guests/<guest_id> - elimina un invitado

con esos endpoints puede administrar guests para eventos especificos del sistema
"""

# usar cadenas permite enviar paramatros adicionales con la solicitud HTTP.
GET /guests?event_id=23

# las dos opciones a elejir es XML y JSON, pero el que mejor se integra es JSON
# formato de libro con XML:
<?xml version="1.0" encoding="UTF-8" ?>
<book>
    <title>Python Basics</title>
    <page_count>635</page_count>
    <pub_date>2021-03-16</pub_date>
    <authors>
        <author>
            <name>David Amos</name>
        </author>
        <author>
            <name>Joanna Jablonski</name>
        </author>
        <author>
            <name>Dan Bader</name>
        </author>
        <author>
            <name>Fletcher Heisler</name>
        </author>
    </authors>
    <isbn13>978-1775093329</isbn13>
    <genre>Education</genre>
</book>

# XML utiliza un sistema de etiquetas como contenedor de datos

# ejemplo con JSON
{
    "title": "Python Basics",
    "page_count": 635,
    "pub_date": "2021-03-16",
    "authors": [
        {"name": "David Amos"},
        {"name": "Joanna Jablonski"},
        {"name": "Dan Bader"},
        {"name": "Fletcher Heisler"}
    ],
    "isbn13": "978-1775093329",
    "genre": "Education"
}
# JSON almacena datos en pare key: value.

"""
respuesta de éxito en la respuesta.
como responderan las solicitudes, deben de tener el mismo formato e incluir el estado de respuesta HTTP correcto
"""

get /cars http/1.1
Host: api.example.com
"""
la solicitud se comport de cuatro partes:
1 GET es el tipo de metodo HTTP
2 /cars es el endpoint de la API
3 HTTP/1.1 es la version HTTP
4 Host: api.example.com es el host de la API
"""
# formato JSON en APi
HTTP/1.1 200 OK
Content-Type: application/json
...

[
    {
        "id": 1,
        "make": "GMC",
        "model": "1500 Club Coupe",
        "year": 1998,
        "vin": "1D7RV1GTXAS806941",
        "color": "Red"
    },
    {
        "id": 2,
        "make": "Lamborghini",
        "model":"Gallardo",
        "year":2006,
        "vin":"JN1BY1PR0FM736887",
        "color":"Mauve"
    },
    {
        "id": 3,
        "make": "Chevrolet",
        "model":"Monte Carlo",
        "year":1996,
        "vin":"1G4HP54K714224234",
        "color":"Violet"
    }
]

"""
REST y Python: herramientas. ejemplo de adminstrar una colección de paises
cada pais tendra los siguientes campos:
name - nombre del pais
capitales - capital del pais
area - área del pais en kilometros

la mayoria de los casos, los datos recibidos de una API provienen de una base de datos.
para este caso se usara una lista para almacenar los datos

usar countries como un endpoint y mantener el formato en json
"""

# flask
from flask import Flask, requestm jsonify

app = Flask(__name__)

countries = [
    {'id': 1, 'name': 'Tailandia', 'capital': 'Bangkok', 'area': 51312},
    {'id': 2, 'name': 'Australia', 'capital': 'Canberra', 'area': 761},
    {'id': 3, 'name': 'Egipto': 'capital': 'Cairo', 'area': 1010408},
]

def _find_next_id():
    return max(country['id'] for country in countries) +1

@app.get)'/countries'
def get_countries():
    return jsonify(countries)

@app.post('/countries')
def add_country():
    if request.is_json:
        country = request.get_json()
        country['id'] = _find_next_id()
        countries.append(country)
        return country, 201
    return {'error': 'Request must be JSON'}, 415

export FLASK_APP=main.py
export FLASK_ENV=development
# cambiar FLASK_ENV por FLASK_DEBUG
# solicitar el endpoint /coutries retorna una lista de diccioanrios con todos los elementos
# pasar un argumento en la url?id=2

# enviar solicitudes desde cli con curl
curl -i http://localhost:5000/countries \
    -X POST \
    -H 'Content-Type: application/json' \
    -d '{"name": "Germany", "capital": "Berlin", "area": 357200}'
# envia una peticion para generar un nuevo recurso, al ir a /countries lista todos incluyendo el nuevo recurso

"""
curl:
-X: establece el metodo HTTP para la solicitud
-H: agragar un encabezado a la solicitud
-d: define los datos de la solicitud
"""
# solicitar todos los recursos desde curl GET
curl -i http://localhost:5000/countries

# FastAPI
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
 1289  history | grep -i "curl"
sudo apt update -y && sudo apt install upgrade -y
python3 -m venv ent_virt
source ent_virt/bin/activate
pip3 install --upgrade pip3
python3 -m pip install fastapi pydantic
python3 -m pip install uvicorn


from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

def find_next_id():
    return max(country.country_id for country in countries) +1

class Country(BaseModel):
    country_id: int = Field(defacult_factory=find_next_id, alidas='id')
    name: str
    capital: str
    area: int

countries = [
    Country(id=1, name="Taildandia", capital="Bangkok", area=513120),
    Country(id=2, name="Autralia", capital="Canberra", area=7617930),
    Country(id=3, name="Egipto", capital"Cairo", area=1010400),
]

@app.get("/countries")
async def get_countries:
    return countries

@app.post("/countries", status_code=201)
async def add_country(country: Country):
    countries.append(country)
    return country
# uvicorn name_app:app --reaload
# go to localhost:8000/countries

# crear un nuevo recurso desde curl
curl -i http://localhost:8000/countries \
    -X POST \
    -H 'Content-Type: application/json' \
    -d '{"name": "Alemania", "capital": "Berlin", "area": 357022}' \
    -w '\n'

# request corey shafer
import requests

url = 'https://xkcd/353/'
r = requests.get(url)
print(r)
print(r.text)
# obtener una imagen
url = 'https://imgs.xkcd.com/comics/python.png'
r = requests.get(url)

with open('python.png', 'wb') as f:
    f.write(r.content)
# usar httpbin.org
url = 'https://httpbin.org/get'
r = requests.get(url)
print(r.headers)
# pasar argumetos en get
payload = {'page': 2, 'count': 23}
r = requests.get(url, params=paylaod)
print(r.text)
print(r.url) # retorna la url con los valores despues de ?
# crear un nuevo recurso con post
payload = {'username': 'corey', 'password': 'testing'}
r = requests.post(url, data=payload)
print(r.text)
# acceder a los valores como un dict usando .json()
r_dict = r.json()
print8r_dict['form']

