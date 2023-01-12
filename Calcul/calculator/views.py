from django.shortcuts import render


def calc(request):
	if request.method == 'POST':
		num1 = request.POST['num1']
		num2 = request.POST['num2']
		if 'add' in request.POST:
			res = int(num1) + int(num2)
			return render(request, 'index.html', {'res': res})
		if 'sub' in request.POST:
			res = int(num1) - int(num2)
			return render(request, 'index.html', {'res': res})
		if 'div' in request.POST:
			res = int(num1) / int(num2)
			return render(request, 'index.html', {'res': res})
		if 'mul' in request.POST:
			res = int(num1) * int(num2)
			return render(request, 'index.html', {'res': res})
		if 'pow' in request.POST:
			res = int(num1) ** int(num2)
			return render(request, 'index.html', {'res': res})
		if 'fdiv' in request.POST:
			res = int(num1) // int(num2)
			return render(request, 'index.html', {'res': res})
		if 'rem' in request.POST:
			res = int(num1) % int(num2)
			return render(request, 'index.html', {'res': res})
	return render(request, 'index.html')
