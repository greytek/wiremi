# # Download the helper library from https://www.twilio.com/docs/python/install
# import os
# from twilio.rest import Client
#
# # Set environment variables for your credentials
# # Read more at http://twil.io/secure
# account_sid = "AC3b32d0e584e380d11cc894981b0627be"
# auth_token = "e3eb8f22fd92fa91f19c3d9de65bcbe1"
# verify_sid = "VAc57e407f134ac9e7a39d88455c9b28d0"
# verified_number = "+923124427197"
#
# client = Client(account_sid, auth_token)
#
# verification = client.verify.v2.services(verify_sid) \
#   .verifications \
#   .create(to=verified_number, channel="sms")
# print(verification.status)
#
# otp_code = input("Please enter the OTP:")
#
# verification_check = client.verify.v2.services(verify_sid) \
#   .verification_checks \
#   .create(to=verified_number, code=otp_code)
# print(verification_check.status)