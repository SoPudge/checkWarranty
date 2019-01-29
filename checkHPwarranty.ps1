$uname = read-Host "请输入代理服务器用户名，格式ls\xxx："
$pwd = read-Host "请输入对应密码："
$pwd=ConvertTo-SecureString $pwd -AsPlainText -Force
$cred=New-Object System.Management.Automation.PSCredential($uname,$pwd)
$proxy = "http://proxy.standard.corp:8080"

function hp($sns)
{
    $headers = @{"Content-Type"="application/json"}
    $ssid_url = "https://support.hp.com/cn-zh/checkwarranty/multipleproducts"
    $api_url = "https://support.hp.com/hp-pps-services/os/multiWarranty?ssid="
    
    #将传入sn数组组合成需要发送的json格式
    $temp = 0..($sns.Length-1)
    for($i=0;$i -lt $sns.Length;$i++)
    {
        $temp[$i] = @{"serialNumber"=($sns[$i] | Out-String).Trim();"isoCountryCde"="CN";"lc"="ZH";"cc"="CN";"modelNumber"=""}
    }

    $payload = @{"gRecaptchaResponse"="";"obligationServiceRequests"=$temp}
    $payload_json = $payload | ConvertTo-Json
    #正则表达式获取和iwr获取ssid，并且keepsession
    $r = Invoke-RestMethod -uri $ssid_url -SessionVariable 'session' -Proxy $proxy -ProxyCredential $cred
    $reg = '.*mwsid":"(?<alp>.*)".*'
    $t = $r -match $reg
    $ssid = $Matches.alp

    #更新apiurl
    $api_url = $api_url + $ssid

    #获取信息
    $s = Invoke-RestMethod -Method Post -Headers $headers -Body $payload_json -uri $api_url -WebSession $session
    #write-host $s.productWarrantyDetailsVO.displaySerialNumber
    $result = 0..($sns.Length-1)
    for($i=0;$i -lt $sns.Length;$i++)
    {
        $SerialNumber = $s.productWarrantyDetailsVO.displaySerialNumber[$i]
        $obligationStartDate = $s.productWarrantyDetailsVO.warrantyResultList.obligationStartDate[$i]
        $obligationEndDate = $s.productWarrantyDetailsVO.warrantyResultList.obligationEndDate[$i]

        $result[$i] = @{SN=($SerialNumber|Out-String);start=($obligationStartDate|Out-String);end=($obligationEndDate|Out-String)}
        Write-Host $SerialNumber,$obligationStartDate,$obligationEndDate
        $SerialNumber+" "+$obligationStartDate+" "+$obligationEndDate | Out-File result.txt -Append
    }
}

$sn = Get-Content("sn.txt")
Write-Host "共计"$sn.Length"个序列号需要查询……"
$Array = @()
for ($i=0;$i -lt $sn.Length;$i+=20) 
{
    $Array += ,@($sn[$i..($i+19)])
}
foreach($a in $Array)
{
    hp($a)
}
write-host "按任意键退出"
Read-Host | Out-Null
Exit
