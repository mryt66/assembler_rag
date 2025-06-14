from utils.requests import ATTAPI
from utils.transpiler import PythonToWTranspiler

transpiler = PythonToWTranspiler()
url = "https://meet-tahr-radically.ngrok-free.app/"
atta_object = ATTAPI(url)

response_llm = atta_object.llm("Napisz program który dodaje dwie liczby i zwraca wynik")
