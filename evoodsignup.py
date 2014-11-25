#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Auto Sign UP
#
# Author:      Ashim
#
# Created:     24/05/2013
# Copyright:   (c) Ashim 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from PIL import Image
import random
import predict

global_email='incogdai@gmail.com'
random_password='asterisk123'

def name_list():
    lst=[]
    with open('C:\Python27\captcha_ex\selenium\evood_pr2\listofnames.txt') as f:
        data=f.readlines()
        #a=len(data)

        for op in data:
            strip=op.strip()
            lst.append(strip.lower())

    gen_name=lst[random.randint(1,len(lst))]+str(random.randint(1,1000))
    print gen_name
    return gen_name

def __uwcblog():

    name=name_list()
    driver=webdriver.Firefox()
    driver.get('http://uwcblog.com/registeryotablog.php')

    username=driver.find_element_by_id('user_name')
    username.send_keys(name)

    email=driver.find_element_by_id('user_email')
    email.send_keys(global_email)

    give_username=driver.find_element_by_id('signupuser')
    give_username.click()

    submit=driver.find_element_by_name('submit')
    submit.submit()
    #COULDNOT COMPLETE BECAUSE REQUIRES MEMBERSHIP CODE

def __bcz():

    name=name_list()
    driver=webdriver.Firefox()
    driver.get('http://bcz.com/register/')

    #STEP1
    username=driver.find_element_by_id('signup_username')
    username.send_keys(name)

    email=driver.find_element_by_id('signup_email')
    email.send_keys(global_email)

    password=driver.find_element_by_id('signup_password')
    password.send_keys(random_password)

    confpassword=driver.find_element_by_id('signup_password_confirm')
    confpassword.send_keys(random_password)

    profdetail=driver.find_element_by_id('field_1')
    profdetail.send_keys(name)


def __evood():

    name=name_list()
    driver=webdriver.Firefox()
    driver.get('http://www.evood.com/signup')
    #username
    username=driver.find_element_by_name('username')
    username.send_keys(name)

    #password
    password=driver.find_element_by_name('password')
    password.send_keys(random_password)

    #conirm password
    confpassword=driver.find_element_by_name('confirmpassword')
    confpassword.send_keys(random_password)

    #email
    email=driver.find_element_by_name('email')
    email.send_keys(global_email)

    images=driver.find_elements_by_tag_name('img')
    for image in images:
        if 'captcha.php' in image.get_attribute('src'):
            captcha_image=image
            break
    pixel=captcha_image.location
    size=captcha_image.size
    im=Image.open('D:/foo.png')
    x1=pixel['x']
    y1=pixel['y']

    x2=x1+size['width']
    y2=y1+size['height']
    im=im.crop((x1,y1,x2,y2))
    im.save('D:/bar.png')

    #Captcha
    captcha=driver.find_element_by_name('imagecode')
    captcha.send_keys(predict.predict(im))
    print predict.predict(im)
    #submit button
    submit=driver.find_element_by_name('register')
    #submit.submit()

#__evood()
#__uwcblog()
__bcz()