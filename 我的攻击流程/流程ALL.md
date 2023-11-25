#  流程

## 信息收集

  **WAF识别**

 `wafw00f`​

```
wafw00f https://baidu.com
```

 **指纹识别**

​`whatweb-plus`​

```
.\whatweb.v0.5.5.19.exe  -a 3 -v https://baidu.com/
```

 **获得子域**

​`ksubdomain`​  主动爆破

```
sudo ksubdomain e -d baidu.com  --retry -1 --filename SecLists/Discovery/DNS/dns-Jhaddix.txt
```

​`subfinder`​​ 被动收集

```
subfinder -d baidu.com
```

**寻找真实IP**

​`Bypass_cdn`​

```
python3 scan.py httsp://baidu.com
```

**端口扫描**

​`RustScan`​

```
rustscan --range 1-65535 -a 127.0.0.1  --ulimit 5000 -- -A -sC
```

​`naabu`​

```
naabu -v -host baidu.com
```

**爬虫**

​`gau`​ 定域的已知 URL  //uro为过滤重复或筛选易受攻击url

```
echo "18comic.vip" | gauurl | uro -f vuln
```

​`katana`​

```
katana -d 5 -jc -aff -u https://baidu.com 
```

**JS相关**

​`JSFinder`

```
python3 JSFinder.py -u https://baidu.com 
```

​`URLFinder`​

```
./URLFinder -s all -m 2 -u https://baidu.com
```

**目录枚举与FUZZ**

​`ffuf`​

```
ffuf -v -c -w ../SecDictionary/filelak/H3-5w敏感文件.txt -u 'https://baidu.com/FUZZ' -t 100
```

​`gobuster`​

```
gobuster dir -u https://baidu.com -w ~/wordlists/shortlist.txt -v
```

**参数发现**

​`x8`​

```
x8 -u https://baidu.com/index.php -w ./Arjun/arjun/db/large.txt -X POST
```

​`ParamSpider`​

```
python3 paramspider.py --domain baidu.com --exclude woff,css,js,png,svg,php,jpg --output baidu.txt
```

**其他**

备案号 FOFA 爱企查

‍
