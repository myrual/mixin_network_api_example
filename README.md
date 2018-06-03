# bnet_client_demo_mixin
The bnet client demo written in python to access mixin api

```
curl "http://127.0.0.1:10086/payMixinUser" -X POST -d'mixinID=31367&amount=1.899&memo=curlpay'
```
```

curl "http://127.0.0.1:10086/payUUID" -X POST -d'receipt_uuid=28ee416a-0eaa-4133-bc79-9676909b7b4e&amount=1.199&memo=curlpayuuid'
```

