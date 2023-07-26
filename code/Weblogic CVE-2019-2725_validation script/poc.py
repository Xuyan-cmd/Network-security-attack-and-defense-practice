#CVE-2019-2725-POC
import requests
import optparse
import os

parse = optparse.OptionParser(usage = 'python3 %prog [-h] [-u URL] [-p PORT] [-f FILE]')
parse.add_option('-u','--url',dest='URL',help='target url')
parse.add_option('-p','--port',dest='PORT',help='target port[default:7001]',default='7001')
parse.add_option('-f',dest='FILE',help='target list')

options,args = parse.parse_args()
#print(options)
#验证参数是否完整
if (not options.URL or not options.PORT) and not options.FILE:
        print('Usage:python3 CVE-2019-2725-POC.py [-u url] [-p port] [-f FILE]\n')
        exit('CVE-2019-2725-POC.py:error:missing a mandatory option(-u,-p).Use -h for basic and -hh for advanced help')

filename = '/_async/AsyncResponseService'


def checking(url):
  try:
    response = requests.get(url+filename)
    if response.status_code == 200:
      print('[+] {0} 存在CVE-2019-2725 Oracle weblogic 反序列化远程命令执行漏洞'.format(url))
    else:
      print('[-] {0} 不存在CVE-2019-2725 Oracle weblogic 反序列化远程命令执行漏洞'.format(url))
  except Exception as e:
    print("[-] {0} 连接失败".format(url))
    exit()
if options.FILE and os.path.exists(options.FILE):
  with open(options.FILE) as f:
    urls = f.readlines()
    #print(urls)
    for url in urls:
      url = str(url).replace('\n','').replace('\r','').strip()
      checking(url)
elif options.FILE and not os.path.exists(options.FILE):
  print('[-] {0} 文件不存在'.format(options.FILE))
  exit()
else:
  #上传链接
  url = options.URL+':'+options.PORT
  checking(url)
