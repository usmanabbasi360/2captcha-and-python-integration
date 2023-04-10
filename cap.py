# sensitive
# ---import necessary libraries

from config import API_KEY
from twocaptcha import TwoCaptcha
import requests, lxml
from bs4 import BeautifulSoup

solver = TwoCaptcha(API_KEY)
data_sitekey="6LfGNEoeAAAAALUsU1OWRJnNsF1xUvoai0tV090n" # from the captcha page 

# ---url of the captcha page 
url = 'https://www.scrapebay.com/spam'

# ---getting csrf and cookies from the first page 
def get_csrf_cookie(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_el = soup.select_one('[name=csrfmiddlewaretoken]')
    # print()
    csrf = csrf_el['value']
    print(f'csrf  -- {csrf}')
    cookies = response.cookies
    return csrf, cookies

# ---funtion to solve captcha , we will send the url, and the sitekwy
def solve(url):
    try:
        result = solver.recaptcha(sitekey= data_sitekey, url = url)
    except:
        result = '--'
        print('failed too solve the captcha')

    return result.get('code')

# --- function to send the post req to the content page along with csrf, cookies, and results
def post_page(url, csrf, cookie, result):
    payload = "csrfmiddlewaretoken={}&g-recaptcha-response{}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.scrapebay.com'
    }
    response= requests.get(url,
                          data=payload.format(csrf, result), 
                          headers=headers, 
                          cookies=cookie)
    soup = BeautifulSoup(response.text, 'lxml')
    # print(soup)
    el = soup.select_one('h1').get_text()
    return el
    
def main():
    csrf, cookie = get_csrf_cookie(url)
    # print(csrf, cookie)
    result = solve(url)
    print(f'catcha-data {result}')
    data = post_page(url, csrf, cookie, result)
    print(data)

if __name__=='__main__':
    main()