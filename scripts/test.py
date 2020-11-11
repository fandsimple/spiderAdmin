import requests

headers = {
    'authority': 'translate.google.cn',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'x-client-data': 'CJa2yQEIpLbJAQjBtskBCKmdygEIq8fKAQj1x8oBCOnIygEItMvKAQjb1coBCJWZywEIx5nLAQiXmssBGPbAygEYisHKAQ==',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'NID=204=ZCf7sRbpXBpdOQ3_pdfkaUH2KBxejeLR75_kKNtxZ0XiKF-q53ZzOtgQrH4Y5GGecVlYfDcyYDMw5gmMilXOxad8lqch18zeh5CSFJUJBcecFniLLJGkwKYwAgfV0sehoGhNkv6r_1iKfUIS3hNeR6dOJX885HvMH5HLTGxEDqc; OTZ=5692538_24_24__24_; _ga=GA1.3.1660380260.1604283871; _gid=GA1.3.1283228848.1604283871',
}

response = requests.get('https://translate.google.cn/', headers=headers)
print(response.text)
