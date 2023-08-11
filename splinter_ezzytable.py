from splinter import Browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint, choice

import os


import argparse

from argparse import RawTextHelpFormatter

screenshot_count = 0

def handle_errors(e):
    #TODO: HANDLE ERRORS
    print(str(e))
    exit()
        
def close_browser(browser):
    try:
        browser.quit()    
    except Exception as e:
        handle_errors(e)


def wait_time(min_actions_wait_time, max_actions_wait_time):
    try:
        
        actions_wait_time = randint(min_actions_wait_time,max_actions_wait_time)
        
        time.sleep(actions_wait_time)
        
    except Exception as e:
        handle_errors(e)
        
def save_screenshot(browser):
    try:
        global screenshot_count   
        global save_ss

        if (save_ss):
            pid = os.getpid()
            screenshot_count += 1
            browser.driver.save_screenshot("ss_"  + str(pid) + "_" + str(screenshot_count) + ".png")
        
    except Exception as e:
        handle_errors(e)

def main():

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('target_url', help='URL to click on Google search results')
    parser.add_argument('-k', '--keyword', help='Keyword to search on google')
    
    parser.add_argument('--min_wait_time', help='Minimum time to generate wait time between browsing actions (seconds)', type=int, default=5)
    parser.add_argument('--max_wait_time', help='Maximum time to generate wait time between browsing actions (seconds)', type=int, default=15)

    parser.add_argument('--max_internal_nav', help='Maximum internal navigation (Must be more than 3)', type=int, default=5)

    parser.add_argument('-u', '--user_agent', default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', help='Web browser user agent string')

    parser.add_argument('-r', '--resolution', default='1366x768', help='Screen resolution: a string containing width an height values separated by the *x* character, i.e. 1366x768.')

    parser.add_argument('--incognito', action='store_true', help='Enables incognito mode')
    parser.add_argument('--headless', action='store_true', help='Enables headless mode')    
    parser.add_argument('--screenshots', action='store_true', help='Enables screenshots')
    parser.add_argument('--debug', action='store_true', help='Enables Console Messages')                
        
    args = parser.parse_args()

    if(args.debug):
        print("Starting")
        print(args)

    #Setting Browser Options
    try:
        size_x = int(args.resolution.lower().split("x")[0])
        size_y = int(args.resolution.lower().split("x")[1])
    except:
        size_x = 1366
        size_y = 768
        
    res = str(size_x) + "," + str(size_y)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--window-size=%s' % res)
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')    
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument('--disable-gpu')    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})


    if(args.debug):
        print("Opening Web Browser")
        
    browser = Browser("chrome", headless=args.headless, incognito=args.incognito, user_agent=args.user_agent, options=chrome_options)    
    wait_time(args.min_wait_time, args.max_wait_time)
    browser.driver.set_window_size(size_x,size_y)
    browser.driver.maximize_window()
    browser.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")            
    browser.driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": args.user_agent}) 
    wait_time(args.min_wait_time, args.max_wait_time)        

    if(args.debug):
        print("Going to https://ipinfo.io/json")
        
    browser.visit("https://ipinfo.io/json")
    wait_time(args.min_wait_time, args.max_wait_time)        

    if(args.debug):    
        if(browser.find_by_tag('body')):
            print("IP info: ",browser.find_by_tag('body').text)
            
    if(args.debug):
        print("Going to Google")
    
    browser.visit("https://www.google.com/")
    wait_time(args.min_wait_time, args.max_wait_time)        

    if (browser.is_element_present_by_xpath("//div[contains(text(),'Aceptar todo')]")):
        if(browser.find_by_xpath("//div[contains(text(),'Aceptar todo')]").last.visible):

            if (browser.is_element_present_by_xpath("//div[contains(text(),'Leer más')]")):
                if(browser.find_by_xpath("//div[contains(text(),'Leer más')]").last.visible):
                    browser.find_by_xpath("//div[contains(text(),'Leer más')]").last.click()    
                    wait_time(args.min_wait_time, args.max_wait_time)        
                    
            wait_time(args.min_wait_time, args.max_wait_time)        
            browser.find_by_xpath("//div[contains(text(),'Aceptar todo')]").last.click()    
            wait_time(args.min_wait_time, args.max_wait_time)        
            
    if args.keyword:
        kw = '"' +args.keyword + '" ' + args.target_url
    else:
        kw = args.target_url

    if(args.debug):
        print("Searching keyword and target url")
        
    browser.fill('q',  kw )

    wait_time(args.min_wait_time, args.max_wait_time)        
    active_web_element = browser.driver.switch_to.active_element
    active_web_element.send_keys(Keys.ENTER)
    wait_time(args.min_wait_time, args.max_wait_time)        
    
    cont = True
    
    while(cont):    

        links_found = browser.links.find_by_partial_href(args.target_url)
        
        if(links_found):
        
            selected_link = choice(links_found) 
            
            if(args.debug):
                if(selected_link):            
                    print("Scrolling To Link: %s" % selected_link["href"] )
            
            if(selected_link["href"]):
                if (browser.is_element_present_by_xpath("//a[@href='" + selected_link["href"]  + "']")):

                    browser.driver.execute_script("var element = document.querySelectorAll('a[href=\"" + selected_link["href"] + "\"]'); element[0].scrollIntoView({block: 'center', behavior: 'smooth'});")        
                    
                    wait_time(args.min_wait_time, args.max_wait_time)        
                
                
                    if(browser.find_by_xpath("//a[@href='" + selected_link["href"]  + "']").first.visible):
                        
                        if(args.debug):
                            print("Opening Link: %s" % selected_link["href"] )
                            
                        browser.find_by_xpath("//a[@href='" + selected_link["href"]  + "']").first.click()
                        cont = False                        
                        
                        wait_time(args.min_wait_time, args.max_wait_time)        

                        internal_nav = randint(3,args.max_internal_nav)
                        internal_nav_count = 0
                        
                        if(args.debug):
                            print("Randomly Browsing Internal Site %s Times." % (str(internal_nav)))
                        
                        while  (internal_nav_count < internal_nav):

                            if (browser.is_element_present_by_xpath("//button[@aria-label='Consent']")):
                                if(browser.find_by_xpath("//button[@aria-label='Consent']").first.visible):
                                    browser.find_by_xpath("//button[@aria-label='Consent']").first.click()
                                    wait_time(args.min_wait_time, args.max_wait_time)                    
                        
                            if (browser.is_element_present_by_xpath("//button[@aria-label='Accept All']")):
                                if(browser.find_by_xpath("//button[@aria-label='Accept All']").first.visible):
                                    browser.find_by_xpath("//button[@aria-label='Accept All']").first.click()
                                    wait_time(args.min_wait_time, args.max_wait_time)        

                            if (browser.is_element_present_by_xpath("//a[@id='king-cookie-accept']")):
                                if(browser.find_by_xpath("//a[@id='king-cookie-accept']").first.visible):
                                    browser.find_by_xpath("//a[@id='king-cookie-accept']").first.click()
                                    wait_time(args.min_wait_time, args.max_wait_time)

                            if (internal_nav_count == 0):
                            
                                wait_time(args.min_wait_time, args.max_wait_time)        
                                if(args.debug):
                                    print("Clicking On Site Logo To Ensure Flow From HomePage")
                                    
                                if (browser.is_element_present_by_xpath("//a[@class='king-logo']")):
                                    browser.find_by_xpath("//a[@class='king-logo']").first.click()
                                    wait_time(args.min_wait_time, args.max_wait_time)        
                                      
                            page_links = browser.find_by_xpath("//a[@class='featured-title']")                    
                            links_found = browser.links.find_by_partial_href('ezzytable.com')
                            selected_link = choice(links_found) 
                            
                            if(args.debug):    
                                print("Scrolling Link: %s" % selected_link["href"] )
                            
                            if(selected_link["href"]):
                                                    
                                if (browser.is_element_present_by_xpath("//a[@href='" + selected_link["href"]  + "']")):
                                
                                    try:

                                        browser.driver.execute_script("var element = document.querySelectorAll('a[href=\"" + selected_link["href"] + "\"]'); element[0].scrollIntoView({block: 'center', behavior: 'smooth'});")        
                                        
                                        wait_time(args.min_wait_time, args.max_wait_time)        
                                    
                                    
                                        if(browser.find_by_xpath("//a[@href='" + selected_link["href"]  + "']").first.visible):
                                            
                                            if(args.debug):
                                                print("Opening Link: %s" % selected_link["href"] )
                                                
                                            browser.find_by_xpath("//a[@href='" + selected_link["href"]  + "']").first.click()
                                            
                                            wait_time(args.min_wait_time, args.max_wait_time)        
                                            
                                            if(args.debug):
                                                print("Scrolling To Bottom On Opened Link" )
                                                
                                            browser.driver.execute_script("window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });")
                                            
                                            internal_nav_count = internal_nav_count + 1
                                            
                                            if(args.debug):
                                                print("Internal Nav Count %"%str(internal_nav_count))
                                            
                                            wait_time(args.min_wait_time, args.max_wait_time)        
                                            
                                            if(args.debug):
                                                print("Going Back To Main Page." )
                                                
                                            browser.back()
                                            
                                            wait_time(args.min_wait_time, args.max_wait_time)        
                                    except:
                                        pass
            else:
            
                if (browser.is_element_present_by_id('pnnext')):        
                    if(args.debug):
                        print("Clicking on Google's next result page.")
                
                    browser.driver.execute_script("var element = document.querySelectorAll('a[id=\"pnnext\"]'); element[0].scrollIntoView({block: 'end', behavior: 'smooth'});")            
                    browser.find_by_id("pnnext").first.click()
                    wait_time(args.min_wait_time, args.max_wait_time)        
                else:
                    cont = False
                    if(args.debug):
                        print("ERROR: No more pages. Target URL not found!")
    else:
    
        if(args.debug):
            print("ERROR: Google results not found!" )
    
    if(args.debug):
        print("Stoping." )
            
    close_browser(browser)
    exit()
    

if __name__ == "__main__":
    main()
