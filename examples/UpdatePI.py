#! /usr/bin/env python

"""
Copyright notice:
(c) Copyright 2024 RocketGate
All rights reserved.

The copyright notice must not be removed without specific, prior
written permission from RocketGate.

This software is protected as an unpublished work under the U.S. copyright
laws. The above copyright notice is not intended to effect a publication of
this work. This software is the confidential and proprietary information of RocketGate.
Neither the binaries nor the source code may be redistributed without prior
written permission from RocketGate.

The software is provided "as-is" and without warranty of any kind, express, implied
or otherwise, including without limitation, any warranty of merchantability or fitness
for a particular purpose. In no event shall RocketGate be liable for any direct,
special, incidental, indirect, consequential or other damages of any kind, or any damages
whatsoever arising out of or in connection with the use or performance of this software,
including, without limitation, damages resulting from loss of use, data or profits, and
whether or not advised of the possibility of damage, regardless of the theory of liability.
"""

import time
import sys
import os

from RocketGate import *


the_time = str(int(time.time()))

cust_id = the_time + ".PythonTest"
inv_id = the_time + ".UpdatePITest"
merch_id = "1"
merch_password = "testpassword"

request = GatewayRequest()
response = GatewayResponse()
service = GatewayService()

#
#	Setup the only request.
#
request.Set(GatewayRequest.MERCHANT_ID, merch_id)
request.Set(GatewayRequest.MERCHANT_PASSWORD, merch_password)

request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

request.Set(GatewayRequest.AMOUNT, 1.00)
request.Set(GatewayRequest.CURRENCY, "USD")
request.Set(GatewayRequest.REBILL_FREQUENCY, "MONTHLY")

request.Set(GatewayRequest.CARDNO, "4111111111111111")
request.Set(GatewayRequest.EXPIRE_MONTH, "02")
request.Set(GatewayRequest.EXPIRE_YEAR, "2030")
request.Set(GatewayRequest.CVV2, "999")

request.Set(GatewayRequest.CUSTOMER_FIRSTNAME, "Joe")
request.Set(GatewayRequest.CUSTOMER_LASTNAME, "PythonTester")
request.Set(GatewayRequest.USERNAME, "pythontest_user")
request.Set(GatewayRequest.CUSTOMER_PASSWORD, "pythontest_pass")
request.Set(GatewayRequest.EMAIL, "pythontest@fakedomain.com")

#
#      Setup test parameters in the service.
#
service.SetTestMode(1)

#
#      Perform the Purchase transaction.
#
if service.PerformPurchase(request, response):
    print("Purchase succeeded")
    print("GUID: ", response.Get(GatewayResponse.TRANSACT_ID))

    # Update Personal Information
    ##
    ##  This would normally be two separate processes, 
    ##  but for example's sake is in one process (thus we clear and set a new GatewayRequest object)
    ##  The key values required are MERCHANT_CUSTOMER_ID and MERCHANT_INVOICE_ID.
    ## 
    request = GatewayRequest()
    request.Set(GatewayRequest.MERCHANT_ID, merch_id)
    request.Set(GatewayRequest.MERCHANT_PASSWORD, merch_password)

    request.Set(GatewayRequest.MERCHANT_CUSTOMER_ID, cust_id)
    request.Set(GatewayRequest.MERCHANT_INVOICE_ID, inv_id)

    request.Set(GatewayRequest.EMAIL, "pythontest_updated@fakedomain.com")
    request.Set(GatewayRequest.USERNAME, "pythontest_user_updated")
    request.Set(GatewayRequest.CUSTOMER_PASSWORD, "pythontest_pass_updated")

    if service.PerformRebillUpdate(request, response):
        print("\nUpdate PI succeeded")

    else:
        print("\nUpdate PI failed")
        print("  Reason Code: ", response.Get(GatewayResponse.REASON_CODE))

else:
    print("Test Purchase failed\n")
    print("GUID: ", response.Get(GatewayResponse.TRANSACT_ID))
    print("Reason Code: ", response.Get(GatewayResponse.REASON_CODE))
    print("Exception: ", response.Get(GatewayResponse.EXCEPTION))
    print("Scrub: ", response.Get(GatewayResponse.SCRUB_RESULTS))
    exit()
