#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# f1r3K0
import requests
import base64
import random
import argparse
from simhashx import simhash

# cookie = ''
res_404 = []


def get_headers():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'Cookie': cookie
    }
    return headers


def random_str():
    ran = random.random() * 100
    return base64.b64encode(str(ran).encode()).decode().replace('=', '')


def is_similar_page(res1, res2, radio=0.85):
    if res1 is None or res2 is None:
        return False
    body1 = res1.text
    body2 = res2.text
    simhash1 = simhash(body1.split())
    simhash2 = simhash(body2.split())
    calc_radio = simhash1.similarity(simhash2)
    if calc_radio > radio:
        return True
    else:
        return False


def generate_404(domain_url):
    ran_str = random_str()
    generate_404_url = domain_url + '/' + ran_str
    print('*** Now is generate_404: ' + generate_404_url)
    headers = get_headers()
    resp_404 = requests.get(generate_404_url, verify=True, headers=headers, timeout=3)
    resp_200 = requests.get(domain_url, verify=True, headers=headers, timeout=3)
    res_404.append(resp_404)
    if is_similar_page(resp_200, resp_404):
        print('*** 404 page is similar to index page.')
        print('*** Maybe have waf.')
        # res_404.append(resp_200)


def is_404(res):
    if res.status_code == 404:
        return True
    for resp_404 in res_404:
        if is_similar_page(res, resp_404):
            return True
    return False


def file_scan(domain_url):
    headers = get_headers()
    results = []
    payloads = ["/robots.txt", "/README.md", "/crossdomain.xml", "/.git/config", "/.svn/entries", "/.svn/wc.db",
                "/.DS_Store", "/CVS/Root", "/CVS/Entries", "/.idea/workspace.xml"]
    payloads += ["/index.htm", "/index.html", "/index.php", "/index.asp", "/index.aspx", "/index.jsp", "/index.do",
                 "/index.action", "/index.phps", "/index.php~", "/.index.php", "/index.php.bak", "/.index.php.swf", "/.index.php.swp", "/upload.php", "/config.php"]
    payloads += ["/www/", "/console", "/web-console", "/web_console", "/jmx-console", "/jmx_console",
                 "/JMXInvokerServlet", "/invoker"]
    payloads += ["/index.bak", "/index.swp", "/index.old", "/.viminfo", "/.bash_history", "/.bashrc",
                 "/project.properties", "/config.properties", "/config.inc", "/common.inc", "/db_mysql.inc",
                 "/install.inc", "/conf.inc", "/db.inc", "/setup.inc", "/init.inc", "/config.ini", "/php.ini",
                 "/info.ini", "/setup.ini", "/www.ini", "/http.ini", "/conf.ini", "/core.config.ini", "/ftp.ini",
                 "/data.mdb", "/db.mdb", "/test.mdb", "/database.mdb", "/Database.mdf", "/BookStore.mdf", "/DB.mdf"]
    payloads += ["/1.sql", "/install.sql", "/schema.sql", "/mysql.sql", "/dump.sql", "/users.sql", "/update.sql",
                 "/test.sql", "/user.sql", "/database.sql", "/sql.sql", "/setup.sql", "/init.sql", "/login.sql",
                 "/backup.sql", "/all.sql", "/passwd.sql", "/init_db.sql"]
    payloads += ["/fckstyles.xml", "/Config.xml", "/conf.xml", "/build.xml", "/web.xml", "/test.xml", "/ini.xml",
                 "/www.xml", "/db.xml", "/database.xml", "/admin.xml", "/login.xml", "/sql.xml", "/sample.xml",
                 "/settings.xml", "/setting.xml", "/info.xml", "/install.xml", "/php.xml", "/.mysql_history"]
    payloads += ["/nginx.conf", "/httpd.conf", "/test.conf", "/conf.conf", "/local.conf", "/user.txt", "/LICENSE.txt",
                 "/sitemap.xml", "/username.txt", "/pass.txt", "/passwd.txt", "/password.txt", "/.htaccess",
                 "/web.config", "/app.config", "/log.txt", "/config.xml", "/CHANGELOG.txt", "/INSTALL.txt",
                 "/error.log"]
    payloads += ["/login", "/phpmyadmin", "/pma", "/pmd", "/SiteServer", "/admin", "/Admin/", "/manage", "/manager",
                 "/manage/html", "/resin-admin", "/resin-doc", "/axis2-admin", "/admin-console", "/system", "/wp-admin",
                 "/uc_server", "/debug", "/Conf", "/webmail", "/service", "/ewebeditor"]
    payloads += ["/xmlrpc.php", "/search.php", "/install.php", "/admin.php", "/regist.php", "/login.php", "/l.php",
                 "/phpinfo.php", "/info.php", "/setup.php", "/forum.php", "/sql.php", "/flag.php", "/getflag.php"]
    payloads += ["/portal", "/blog", "/bbs", "/webapp", "/webapps", "/plugins", "/cgi-bin", "/htdocs", "/wsdl", "/html",
                 "/install", "/test", "/tmp", "/file", "/solr/#/", "/WEB-INF", "/zabbix", "/backup", "/log", "/test"]
    payloads += ["/www.7z", "/www.rar", "/www.zip", "/www.tar.gz", "/wwwroot.zip", "/wwwroot.rar", "/wwwroot.7z",
                 "/wwwroot.tar.gz", "/backup.7z", "/backup.rar", "/backup.tar", "/backup.tar.gz", "/backup.zip",
                 "/index.7z", "/index.rar", "/index.sql", "/index.tar", "/index.tar.gz", "/index.zip"]
    if domain_url[-1:] == '/':
        domain_url = domain_url[:-1]
    try:
        generate_404(domain_url)
        for payload in payloads:
            try:
                res = requests.get(domain_url + payload, verify=True, headers=headers, timeout=3)
                if is_404(res) is False:
                    print('Found! Get %s 200' % (domain_url+payload))
                    results.append(payload)
            except:
                pass
    except:
        pass
    if len(results) > 40:
        print('*** Maybe have waf.')
        return '[]'
    else:
        return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-u", "--url", action="store", help="Target URL (e.g. 'http://www.site.com')")
    group.add_argument("-l", "--list", action="store", help="URL list file (e.g. 'targets.txt')")
    args = parser.parse_args()
    if args.url:
        result = file_scan(args.url)
        print(result)
    elif args.list:
        result = {}
        filename = args.list
        with open(filename) as f:
            for line in f:
                line = line.rstrip("\n")
                _result = file_scan(line)
                result[line] = _result
        for key in result:
            print('[+] ' + key)
            print('[+] ' + str(result[key]))
    else:
        print("error: missing a mandatory option (-u or -l), use -h for basic help")
