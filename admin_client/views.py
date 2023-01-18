from django.shortcuts import render,HttpResponse


# Create your views here.

def Home(request):


    return render(request, "clientadmin/product_tab.html")

def Rights(request):
    if request.method == "POST":
        products = request.POST.get("product")
        return HttpResponse(products)
    return render(request, "clientadmin/right.html")