from django.http import HttpResponse
from django.http import HttpRequest
import json

#simple View
def hello_world(request):
    print(request.method)
    return HttpResponse('Hello, world!')

# Uso de GET and POST request.method
def numbers(request):
    if request.method == 'GET':
        print("el metodo usado fue: ", f"{request}", f"{request.method}")
    elif request.method == 'POST':
        print("el metodo usado fue: ", f"{request}", f"{request.method}")

    print(request.GET['numbers'])
    
    get_numbers = request.GET["numbers"]
    get_numbers = map(int, get_numbers.split(","))
    get_numbers = sorted(get_numbers)[::-1]
    data = {
        'status': 'ok',
        'numbers': get_numbers,
        "message": "Integers sorted successfully",

    }
    response = json.dumps(data, indent=4)
    return HttpResponse(response, content_type='application/json')
    

# Pasando argumentos por URL
def say_hi(request, name, age):
    """
    view say_hi
    """
    if age < 12:
        message = f"Sorry {name}, you are not allowed here"
    else:
        message = f"Hello {name}!, Welcome to Firstapp!"

    return HttpResponse(message)
