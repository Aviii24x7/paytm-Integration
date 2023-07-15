from django.shortcuts import render
from .models import User
from .forms import UserForm
from payToMe.settings import PAYTM_MERCHANT_ID, PAYTM_MERCHANT_KEY
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_200_OK
from django.http.response import JsonResponse

import requests
import json
import base64
from paytmchecksum import PaytmChecksum

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/
# import PaytmChecksum
import string, random

# Create your views here.
def generate_id(length=50):
    key=""
    for i in range(length):
        key+=random.choice(string.ascii_lowercase + string. ascii_uppercase +string.digits)
    return key

def starting_page(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            # form=UserForm()
            amount= int(request.POST.get("amount"))
            email= request.POST.get("email")

        # instobj=User.objects.last()
        order_id=generate_id()
        print("\n\n\n==========ORDER ID IS"+ order_id)
        paytmParams = dict()

        paytmParams["body"] = {
            "requestType"   : "Payment",
            "mid"           : PAYTM_MERCHANT_ID,
            "websiteName"   : "WEBSTAGING",
            "orderId"       : order_id,
            "callbackUrl"   : "http://127.0.0.1:8000/handle-request",
            "txnAmount"     : {
                "value"     : "1.00",
                "currency"  : "INR",
            },
            "userInfo"      : {
                "custId"    : email,
            },
        }

        # Generate checksum by parameters we have in body
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)
    
        print("\n\n\n============CHECKSUM IS: " + checksum)
        paytmParams["head"] = {
            "signature"    : checksum
        }
        print("\n\n\n-----------PAYTMPARAMS IS: ")
        print(paytmParams)

        post_data = json.dumps(paytmParams)

        print("\n\n\n-----------POSTDATA IS: ")
        print(post_data)

        # for Staging
        url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={}&orderId={}"

        # for Production
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
        response = requests.post(url.format(PAYTM_MERCHANT_ID,order_id), data = post_data, headers = {"Content-type": "application/json"}).json()
        print("\n\n\n----------RESPOMSE IS:")
        print(response)

        payment_page={
            "mid":PAYTM_MERCHANT_ID,
            "txnToken":response['body']['txnToken'],
            "orderId":order_id
        }

        return render(request,"paytmredirect.html",context={ 'txnData':payment_page})

    form=UserForm()
    return render(request,"home.html",context={'form':form})
    
    
    
    
    
@csrf_exempt
def handle_callback(request):
    form = request.POST
    param_dict= {}

    order_id=request.POST.get('ORDERID')
    payment_mode= request.POST.get('PAYMENTMODE')
    transaction_id=request.POST.get('TXNID')
    bank_transaction_id=request.POST.get('BANKTXNID')
    transaction_date=request.POST.get('TXNDATE')

    res_msg= request.POST.get('RESPMSG')
    context={'error_message':res_msg}
    
    if res_msg!= 'Txn Success':
        return render(request,"paymentsuccess.html", context)

    for i in form.keys():
        param_dict[i]=form[i]

    checksum=request.POST.get('CHECKSUMHASH')
    isVerifySignature = PaytmChecksum.verifySignature(param_dict,PAYTM_MERCHANT_KEY,checksum)
        
    if isVerifySignature==False:
        return render(request,"paymentfail.html")
        
    return render(request,"paymentsuccess.html")

