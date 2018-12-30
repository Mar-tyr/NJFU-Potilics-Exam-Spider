import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import os.path as osp


def fetch_exams(outpath, uname, pw, from_id, to_id):
    driver = webdriver.Chrome()
    driver.get("http://202.119.208.57/")

    username = driver.find_element_by_id('j_idt12:urn')
    username.clear()
    username.send_keys(uname)

    passwd = driver.find_element_by_id('j_idt12:pwd')
    passwd.clear()
    passwd.send_keys(pw)

    login_btn = driver.find_element_by_id('j_idt12:login')
    login_btn.send_keys(Keys.RETURN)

    for i in range(from_id, to_id):
        enter_exam_btn = driver.find_element_by_id('myForm:j_idt114')
        enter_exam_btn.send_keys(Keys.RETURN)

        start_exam_btn = driver.find_element_by_id('myForm:examDc:0:j_idt156')
        start_exam_btn.send_keys(Keys.RETURN)

        time.sleep(2.5)
        submit_exam_btn = driver.find_element_by_id('myForm:presubcase11')
        submit_exam_btn.send_keys(Keys.RETURN)

        verify_submit_btn = driver.find_element_by_id('myForm:j_idt19')
        verify_submit_btn.send_keys(Keys.RETURN)

        details_btn = driver.find_element_by_id('j_idt5:j_idt19')
        details_btn.send_keys(Keys.RETURN)

        html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        with open('{}/{}.html'.format(outpath, i), 'w') as fp:
            fp.write(html.encode('utf-8'))
        print '{}.html done!'.format(i)
        driver.get('http://202.119.208.57/talk/Default.jspx')

    driver.close()


def parse_exam():
    pass


if __name__ == '__main__':
    outpath = 'marx'
    if not osp.isdir(outpath):
        os.mkdir(outpath)

    fetch_exams(outpath, '170201102', '123456', 0, 900)
