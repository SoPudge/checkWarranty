#### Quickly check HP warranty status
Access https://support.hp.com/us-en/checkwarranty/multipleproducts/ and find the mwsid from source,like below

```html
<input type="hidden" id="secureFieldJson" value='{"mwsid":"7e4eed8c-66a3-4fa9-84af-d905bd2a8ee1"}' />
```

Fill the mwsid into this url and post the JSON body(format like below) to url like below
```html
https://support.hp.com/hp-pps-services/os/multiWarranty?ssid=
```
1. headers
```html
Content-Type"="application/json
```
1. JSON Body like below
```json
{
    "obligationServiceRequests":  [
                                      {
                                          "serialNumber":  "4CV6010FGW",
                                          "modelNumber":  "",
                                          "lc":  "ZH",
                                          "isoCountryCde":  "CN",
                                          "cc":  "CN"
                                      },
                                      {
                                          "serialNumber":  "6CR6459M4M",
                                          "modelNumber":  "",
                                          "lc":  "ZH",
                                          "isoCountryCde":  "CN",
                                          "cc":  "CN"
                                      },
                                      {
                                          "serialNumber":  "6CR7082XPP",
                                          "modelNumber":  "",
                                          "lc":  "ZH",
                                          "isoCountryCde":  "CN",
                                          "cc":  "CN"
                                      },
                                      {
                                          "serialNumber":  "6CR7082XPQ",
                                          "modelNumber":  "",
                                          "lc":  "ZH",
                                          "isoCountryCde":  "CN",
                                          "cc":  "CN"
                                      }
                                  ],
    "gRecaptchaResponse":  ""
}
```

1. You will have a JSON respond about the warranty status
