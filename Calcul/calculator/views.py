from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from calculator.models import CalcResponse


def home(request):
	return render(request, 'index.html')


@login_required
def calc(request):
	p = Paginator(CalcResponse.objects.all().order_by('-created_at'), 6)
	page = request.GET.get('page')
	rendering = p.get_page(page)
	nums = "a" * rendering.paginator.num_pages
	if request.method == 'POST':
		num1 = request.POST.get('num1')
		num2 = request.POST.get('num2')
		try:
			if 'add' in request.POST:
				res = int(num1) + int(num2)
				CalcResponse.objects.create(user=request.user, num1=num1, symbol='+', num2=num2, calc_answer=res)
				return render(request, 'calc.html', {'res': res, 'rendering': rendering, 'nums': nums})
			if 'sub' in request.POST:
				res = int(num1) - int(num2)
				CalcResponse.objects.create(user=request.user, num1=num1, symbol='-', num2=num2, calc_answer=res)
				return render(request, 'calc.html', {'res': res, 'rendering': rendering, 'nums': nums})
			if 'div' in request.POST:
				res = int(num1) / int(num2)
				CalcResponse.objects.create(user=request.user, num1=num1, symbol='/', num2=num2, calc_answer=res)
				return render(request, 'calc.html', {'res': res, 'rendering': rendering, 'nums': nums})
			if 'mul' in request.POST:
				res = int(num1) * int(num2)
				CalcResponse.objects.create(user=request.user, num1=num1, symbol='*', num2=num2, calc_answer=res)
				return render(request, 'calc.html', {'res': res, 'rendering': rendering, 'nums': nums})
			if 'pow' in request.POST:
				res = int(num1) ** int(num2)
				CalcResponse.objects.create(user=request.user, num1=num1, symbol='**', num2=num2, calc_answer=res)
				return render(request, 'calc.html', {'res': res, 'rendering': rendering, 'nums': nums})
			if 'fdiv' in request.POST:
				res = int(num1) // int(num2)
				CalcResponse.objects.create(user=request.user, num1=num1, symbol='//', num2=num2, calc_answer=res)
				return render(request, 'calc.html', {'res': res, 'rendering': rendering, 'nums': nums})
			if 'rem' in request.POST:
				res = int(num1) % int(num2)
				CalcResponse.objects.create(user=request.user, num1=num1, symbol='%', num2=num2, calc_answer=res)
				return render(request, 'calc.html', {'res': res, 'rendering': rendering, 'nums': nums})
		except ZeroDivisionError:
			return render(request, 'calc.html', {"error": "Can't divide by 0", 'rendering': rendering, 'nums': nums})
		except ValueError:
			return render(request, 'calc.html', {"error": "You need to type two numbers", 'rendering': rendering, 'nums': nums})

	return render(request, 'calc.html', {'rendering': rendering, 'nums': nums})

# @login_required
# def calc(request):
# 	def create_calc_response(user, num1, symbol, num2, calc_answer):
# 		CalcResponse.objects.create(user=user, num1=num1, symbol=symbol, num2=num2, calc_answer=calc_answer)
#
# 	if request.method == 'POST':
# 		try:
# 			num1 = int(request.POST.get('num1'))
# 			num2 = int(request.POST.get('num2'))
# 			operations = {
# 				'add': (num1 + num2, '+'),
# 				'sub': (num1 - num2, '-'),
# 				'div': (num1 / num2, '/'),
# 				'mul': (num1 * num2, '*'),
# 				'pow': (num1 ** num2, '**'),
# 				'fdiv': (num1 // num2, '//'),
# 				'rem': (num1 % num2, '%'),
# 			}
# 			for key, value in operations.items():
# 				if key in request.POST:
# 					res, symbol = value
# 					create_calc_response(request.user, num1, symbol, num2, res)
# 					return render(request, 'calc.html', {'res': res})
# 		except ZeroDivisionError:
# 			return render(request, 'calc.html', {"error": "Can't divide by 0"})
# 		except (ValueError, TypeError):
# 			return render(request, 'calc.html', {"error": "You need to type two numbers"})
# 		except Exception as e:
# 			return render(request, 'calc.html', {"error": str(e)})
# 	return render(request, 'calc.html')

