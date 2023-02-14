from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from calculator.models import CalcResponse


def home(request):
	return render(request, 'index.html')


def delete_res(request, calcresponse_id):
	calcresponse = CalcResponse.objects.get(pk=calcresponse_id)
	calcresponse.delete()
	return redirect('calc')


@login_required()
def calc(request):
	def create_calc_response(user, num1, symbol, num2, calc_answer):
		CalcResponse.objects.create(user=user, num1=num1, symbol=symbol, num2=num2, calc_answer=calc_answer)
	
	p = Paginator(CalcResponse.objects.all().order_by('-created_at'), 6)
	page = request.GET.get('page')
	rendering = p.get_page(page)
	nums = "a" * rendering.paginator.num_pages
	if request.method == 'POST':
		try:
			num1 = int(request.POST.get('num1'))
			num2 = int(request.POST.get('num2'))
			operations = {
				'add': (num1 + num2, '+'),
				'sub': (num1 - num2, '-'),
				'div': (num1 / num2, '/'),
				'mul': (num1 * num2, '*'),
				'pow': (num1 ** num2, '**'),
				'fdiv': (num1 // num2, '//'),
				'rem': (num1 % num2, '%'),
			}
			for key, value in operations.items():
				if key in request.POST:
					res = value[0]
					symbol = value[1]
					create_calc_response(request.user, num1, symbol, num2, res)
					return render(request, 'calc.html', {'res': res, 'rendering': rendering, 'nums': nums})
		except ZeroDivisionError:
			return render(request, 'calc.html', {"error": "Can't divide by 0"})
		except (ValueError, TypeError):
			return render(request, 'calc.html', {"error": "You need to type two numbers"})
		except Exception as e:
			return render(request, 'calc.html', {"error": str(e)})
	return render(request, 'calc.html', {'rendering': rendering, 'nums': nums})

