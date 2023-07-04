from django.shortcuts import render
from .models import User
from .forms import UserForm
from payToMe.settings import PAYTM_MERCHANT_ID, PAYTM_MERCHANT_KEY
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import requests
import json
import base64
from payApp import PaytmChecksum

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
        print(order_id)
        paytmParams = dict()

        paytmParams["body"] = {
            "requestType"   : "Payment",
            "mid"           : PAYTM_MERCHANT_ID,
            "websiteName"   : "WEBSTAGING",
            "orderId"       : str(order_id),
            "callbackUrl"   : "https/127.0.0.1:8000/handle-request/",
            "txnAmount"     : {
                "value"     : str(amount),
                "currency"  : "INR",
            },
            "userInfo"      : {
                "custId"    : str(email) ,
            },
        }

        checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), PAYTM_MERCHANT_KEY)

        # head parameters
        paytmParams["head"] = {

            # put generated checksum value here
            "signature"	: checksum
        }
        
                

        # for Staging
        url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={PAYTM_MERCHANT_ID}&orderId={order_id}"
        post_data = json.dumps(paytmParams)

        # for Production
        # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId="
        response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
        print(response)

        payment_page={
            "mid":PAYTM_MERCHANT_ID,
            "txnToken":response['body']['txnToken'],
            "orderId":paytmParams['body']['orderId']
            
        }

        return render(request,"paytm.html",context={'paytm_params':payment_page, "order_id":paytmParams["body"]["orderId"]})

    form=UserForm()
    return render(request,"home.html",context={'form':form})
    
    
    
    
    
@csrf_exempt
def handle_callback(request):
    
    HttpResponse("done ")


def OAuth_token(request):

    paytmParams = dict()

    paytmParams["grantType"] = "authorization_code"
    paytmParams["cpde"]      = "999e3877-97c1-XXXX-b19d-6c8787983300"
    paytmParams["deviceId"]  = "Device123"

    post_data = json.dumps(paytmParams)

    auth = "Basic " + base64.b64encode("CLIENT_ID" + ":" + "CLIENT_SECRET")

    # for Staging
    url = "https://accounts-uat.paytm.com/oauth2/v3/token/sv1/"

    # for Production
    # url = "https://accounts.paytm.com/oauth2/v3/token/sv1/"
    response = requests.post(url, data = post_data, headers = {"Authorization": auth,"Content-type": "application/json"}).json()
    print(response)   


def initiate_transaction_API(request):

    paytmParams = dict()

    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : PAYTM_MERCHANT_ID,
        "websiteName"   : "WEBSTAGE",
        "orderId"       : "ORDERID_98765",
        "callbackUrl"   : "https://<callback URL to be used by merchant>",
        "txnAmount"     : {
            "value"     : "",
            "currency"  : "INR",
        },
        "userInfo"      : {
            "custId"    : "CUST_001",
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "YOUR_MERCHANT_KEY")

    paytmParams["head"] = {
        "signature"    : checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"

    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    print(response)
    


def fetch_payments(request):
    
    paytmParams = dict()

    paytmParams["head"] = {
        "txnToken" : "f0bed899539742309eebd8XXXX7edcf61588842333227"
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/fetchPaymentOptions?mid=YOUR_MID_HERE&orderId=ORDERID_98765"

    # for Production
    # url = "https://securegw.paytm.in/fetchPaymentOptions?mid=YOUR_MID_HERE&orderId=ORDERID_98765"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    print(response)



def transaction_status(request):
    paytmParams = dict()

    # body parameters
    paytmParams["body"] = {

        # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        "mid" : "YOUR_MID_HERE",

        # Enter your order id which needs to be check status for
        "orderId" : "YOUR_ORDER_ID",
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "YOUR_MERCHANT_KEY")

    # head parameters
    paytmParams["head"] = {

        # put generated checksum value here
        "signature"	: checksum
    }

    # prepare JSON string for request
    post_data = json.dumps(paytmParams)

    # for Staging
    url = "https://securegw-stage.paytm.in/v3/order/status"

    # for Production
    # url = "https://securegw.paytm.in/v3/order/status"

    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()