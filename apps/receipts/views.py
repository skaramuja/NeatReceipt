import base64
import threading

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from matplotlib import pyplot as plt
from pandas import DataFrame

from .api_clients import ReceiptProcessor, VeryfiMockClient, VeryfiClient
from .forms import ReceiptImage, ImageForm
from .models import Receipt, ReceiptItem


@login_required(login_url='/accounts/login/')
def home_view(request):
    """
    Displays the home page after the user has signed in.
    :param request: The HTTP request.
    :return: A view for the home screen.
    """
    if request.method == 'POST':
        return image_upload_view(request)
    return render(request, 'home.html', {})


@login_required(login_url='/accounts/login/')
def image_upload_view(request):
    """
    Process images uploaded by users.
    :param request: The HTTP request.
    :return: A view to display the receipt that was uploaded.
    """
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_receipt = form.save(commit=False)
            new_receipt.user = request.user
            new_receipt.save()
            mock_client = VeryfiMockClient()
            veryfi_client = VeryfiClient()
            image_processor = ReceiptProcessor(veryfi_client)
            t = threading.Thread(target=image_processor.process_document,
                                 args=(new_receipt, 'Groceries', request.user)
                                 )
            t.start()
            return redirect('/receipts')
        else:
            print("Image upload unsuccessful")
            print(form.errors)
    else:
        form = ReceiptImage()
    return render(request, 'receipt/receipt.html', {'receipt': form})


def receipt_view(request, receipt_id):
    """
    Displays a view for the receipt with the corresponding id.
    :param request: The HTTP Request.
    :param receipt_id: Identifier for the receipt to display.
    :return: A view that displays the receipt.
    """
    receipt = Receipt.objects.get(pk=receipt_id)
    receipt_items = ReceiptItem.objects.filter(receipt__pk=receipt_id)
    if receipt is not None:
        context = {
            'receipt': receipt,
            'items': receipt_items,
        }
        return render(request, 'receipt/receipt.html', context)
    else:
        raise Http404("Recept does not exist")


def receipts_view(request):
    """
    Displays a view for the list of users receipts.
    :param request: The HTTP Request.
    :return: A view that displays a list of receipts.
    """
    receipts = Receipt.objects.filter(user__pk=request.user.id)
    return render(request, 'receipt/receipts.html', {'receipts': receipts})


def receipt_delete(request, receipt_id):
    """
    Deletes a receipt with the provided identifier.
    :param request: The HTTP Request.
    :param receipt_id: Identifier for the receipt to delete.
    :return: Redirect to the list of receipts.
    """
    receipt = Receipt.objects.get(id=receipt_id)
    receipt.vendor.delete()
    receipt.delete()

    return redirect('/receipts')


def reports_view(request):
    receipts = Receipt.objects.filter(user__pk=request.user.id)
    dataframe = DataFrame(receipts.values())

    plt.switch_backend('AGG')

    date = dataframe['date'].dt.strftime('%m-%d-%Y')

    total_price = dataframe.groupby('date')['total_price'].agg('sum')
    plt.bar(date, total_price, color='g', align='center', alpha=0.5)

    plt.ylabel('Total Price')
    plt.xlabel('Date')

    plt.title('Total Expenses Over Time')

    plt.savefig('media/barchart.png')
    plt.clf()

    tax = dataframe.groupby('date')['tax'].agg('sum') + dataframe.groupby('date')['subtotal'].agg('sum')
    subtotal = dataframe.groupby('date')['subtotal'].agg('sum')

    tax_bar = plt.bar(date, tax, color='b', label="tax")
    subtotal_bar = plt.bar(date, subtotal, color='r', label="subtotal")
    plt.legend(handles=[subtotal_bar, tax_bar])

    plt.ylabel('Total Price')
    plt.xlabel('Date')

    plt.title('Subtotal vs Tax')

    plt.savefig('media/barchart2.png')
    return render(request, 'report.html')

