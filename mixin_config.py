mixin_client_id = "3c5fd587-5ac3-4fb6-b294-423ba3473f7d"
mixin_client_secret = "757a329337cbcf8904ad59dd56d335f0c6903a9b69a85782e230f4e359b16814"
mixin_pay_pin = '841316'
mixin_pay_sessionid = 'c1530e12-8e92-4b2f-ba78-843cbfdfb148'

private_key = """-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCyKAn69XOASaPsXo5ctWzJPz5KwjKnpXrpSjIQ1KOJtZAZfm0M
CdFPyR4Bp9ff3nlsWZn7UC1lSzvqtDWmo27EwTK9a3/h1YnLCEhd7C7JzM+kpMZM
BUvzO5cbNa9rWpqpxjkqDH1J9TxwPROQMFtWC3rRvnvmhNwrwJEHfEW6KQIDAQAB
AoGAGZSKKlCH7wmj0dKZ2lHqdtLv3MgZgdzO0yRmH+iIOsOpFyACBFJ8jVoxRseU
xX4qLRaId39BpWOyDLcnZO/efYAciC+JO1ZEJKUJZbLVf4ttWLYvXutOz7gFNMe5
nHnmu4en9xBkfw5p81iRDT0eHujNh/6S84sCRByk3oKHAQECQQDtU7TzZ3XON4Dn
G39z/XGV4slwIurk7bBDXeryXNAVR9cb6snTKKelmDSEokQGvfw5CC5b3Dy6JskG
LgjaVgg5AkEAwCyBT/TeTb4NKHcQhUXmvn2/MnWlEPo6S7fHf31eEpSQ32ybvS2w
+iK+WGXSfyo32E/nH4Ka4m/Dt3nso6LhcQJBANz4P1cSUaG8FA0akUUSCZwhGKWM
HWEh3igbXhJjUGtABI09wsUU6WNJoDyOSQBuDFWdxGxLV0+LpUhXvG5uBCECQQCe
kdqd3EK2yXRYCG70WWp9kor6mwJ6UM9bfSi7dPnzwO0NvrN/VT1sGNERZetcDL0J
21ytrnoZD/nh4lQ17gexAkAWCo+nrChinT+X0tYKFe4+Qy4bLIJnfuamdfawgEGH
+5rUpcGQvTkRX3Z6q5yftmTKa3nHRBvusVyh8PNVyC3b
-----END RSA PRIVATE KEY-----"""


mixin_pin_token = """Ha9ACKUcUOkmkfagSVtsVj0/s3aCH2NYW2C0bPMgFlRd8ekzqYuUfhwFkFztB2i/GRjDdW3cLhcpXtw8/xIGTad/YvcMLuxzOREnCnDHopH8JtYvoG/qf4GqLRRcglpgdBSmF20glD5Ia/sbYCuBCZ5h9eN6L9MCqozyGovXrQU="""
admin_uuid = "28ee416a-0eaa-4133-bc79-9676909b7b4e"
class user_mixin_config:
    def __init__(self):
        self.mixin_client_id = ""
        self.mixin_pay_sessionid= ""
        self.mixin_pin_token= ""
        self.mixin_pay_pin = ""
        self.private_key = ""
        self.deviceID = ""
        self.keyForAES = ""
        self.asset_pin = ""
