from django.shortcuts import render


def home(request):
	return render(request, 'index.html')


def calc(request):
	if request.method == 'POST':
		num1 = request.POST['num1']
		num2 = request.POST['num2']
		try:
			if 'add' in request.POST:
				res = int(num1) + int(num2)
				return render(request, 'calc.html', {'res': res})
			if 'sub' in request.POST:
				res = int(num1) - int(num2)
				return render(request, 'calc.html', {'res': res})
			if 'div' in request.POST:
				res = int(num1) / int(num2)
				return render(request, 'calc.html', {'res': res})
			if 'mul' in request.POST:
				res = int(num1) * int(num2)
				return render(request, 'calc.html', {'res': res})
			if 'pow' in request.POST:
				res = int(num1) ** int(num2)
				return render(request, 'calc.html', {'res': res})
			if 'fdiv' in request.POST:
				res = int(num1) // int(num2)
				return render(request, 'calc.html', {'res': res})
			if 'rem' in request.POST:
				res = int(num1) % int(num2)
				return render(request, 'calc.html', {'res': res})
		except ZeroDivisionError:
			return render(request, 'calc.html', {"error": "Can't divide by 0"})
		except ValueError:
			return render(request, 'calc.html', {"error": "You need to type two numbers"})
			
	return render(request, 'calc.html')
