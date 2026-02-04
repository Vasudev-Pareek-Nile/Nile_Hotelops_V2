from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import re
from .models import OrganizationUrls
from django.shortcuts import render
from app.models import OrganizationMaster
from .models import PartnerRating
import time
def setup_driver():
    chrome_options = Options()
    chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scrape_tripadvisor(driver, url):
    data = {}
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ZuFMR.f"))
        )
        span_value = driver.find_element(By.CSS_SELECTOR, ".kJyXc.P").text
        data["Overall Rating"] = span_value
        
        rating_divs = driver.find_elements(By.CSS_SELECTOR, ".ZuFMR.f")
    
        for div in rating_divs:
            # Extract the SVG element and its associated title
            svg_element = div.find_element(By.TAG_NAME, "svg")
            title_element = svg_element.find_element(By.TAG_NAME, "title")
            title_text = title_element.text
            
            # Extract the rating from the title text
            match = re.search(r'(\d+\.\d+)', title_text)
            if match:
                rating = match.group(1)
                # Find the category label
                category_label = div.find_element(By.CSS_SELECTOR, ".CdRej").text
                data[category_label]=rating
            else:
                print("No rating found in title text")

    except TimeoutException:
        print("Timed out waiting for page to load")
    # finally:
    #     driver.quit()
    return data

def scrape_makemytrip(driver, url):
    data = {}
    driver.get(url)
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ovrlRating__rating.blueBg"))
        )
        overall_rating_element = driver.find_element(By.CSS_SELECTOR, ".ovrlRating__rating.blueBg")
        overall_rating = overall_rating_element.text
        data["Overall Rating"] = overall_rating

        ratings = driver.find_elements(By.CSS_SELECTOR, ".ratingCat__listItem")

        for rating in ratings:
            category = rating.find_element(By.CSS_SELECTOR, ".font16").text
            score = rating.find_element(By.CSS_SELECTOR, ".ratingCat__listItemRating").text
            data[category] = score

    except TimeoutException:
        print("Timed out waiting for page to load")
    return data

def scrape_agoda(driver, url):
    data = {}
    driver.get(url)
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a9f68-box > h2 > span.sc-jrAGrp.sc-kEjbxe.fzPhrN.ehWyCi"))
        )
        overall_rating_element = driver.find_element(By.CSS_SELECTOR, ".a9f68-box > h2 > span.sc-jrAGrp.sc-kEjbxe.fzPhrN.ehWyCi")
        overall_rating = overall_rating_element.text
        data['Overall Rating'] = overall_rating
        facility_ratings = driver.find_elements(By.CSS_SELECTOR, ".Box-sc-kv6pi1-0 .a9f68-box > span")
        ratings_dict = {}

        for rating in facility_ratings:
            text = rating.text
            if "Cleanliness" in text or "Service" in text or "Facilities" in text or "Value for money" in text:
                parts = text.rsplit(' ', 1) 
                if len(parts) == 2:
                    category, value = parts
                    ratings_dict[category] = value


        for category, value in ratings_dict.items():
            if value:
                data[category] = value


    except TimeoutException:
        print("Timed out waiting for page to load")
    return data

def scrape_booking(driver, url):
    data = {}
    time.sleep(60)
    driver.get(url)
    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='review-subscore']"))
        )
    
        try:
            overall_rating_element = driver.find_element(By.CSS_SELECTOR, "[data-testid='review-score-component'] .ac4a7896c7")
            overall_rating = overall_rating_element.text.strip().split()[-1]
            data["Overall Rating"] = overall_rating
        except NoSuchElementException:
            print(f"Element not found: {e}")
       
        category_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='review-subscore'] .c72df67c95 .ccb65902b2:not(.bdc1ea4a28)")
        rating_elements = driver.find_elements(By.CSS_SELECTOR, "[data-testid='review-subscore'] .c72df67c95 .ccb65902b2.bdc1ea4a28")

        data_pairs = []
        for i in range(len(category_elements)):
            try:
                category_name = category_elements[i].text.strip()
                rating_value = rating_elements[i].text.strip()
                data[category_name] = rating_value
            except IndexError:
                data[category_name] = "Missing rating"
            except Exception as e:
                print(f"An error occurred: {e}")

    except TimeoutException:
        print("Timed out waiting for page to load")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except StaleElementReferenceException as e:
        print(f"Stale element reference: {e}")
        scrape_booking(driver, url)
    return data

def social_data(source_list):
    organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=True)
    for org in organizations:
        OrganizationID=org.OrganizationID
        main_dict = {}
        try:
            urls = OrganizationUrls.objects.get(OrganizationID=OrganizationID)
        except OrganizationUrls.DoesNotExist:
            print("OrganizationUrls instance not found.")
            urls = None
        
        driver = setup_driver()
        
        if urls:
            try:
                for source in source_list:
                    url = None
                    if source == 'MakeMyTrip':
                        url = urls.makemytrip_url
                        if url:
                            main_dict['MakeMyTrip'] = scrape_makemytrip(driver, url)
                        else:
                            main_dict['MakeMyTrip'] = {"Error": "URL not found"}
                    elif source == 'Agoda':
                        url = urls.agoda_url
                        if url:
                            main_dict['Agoda'] = scrape_agoda(driver, url)
                        else:
                            main_dict['Agoda'] = {"Error": "URL not found"}
                    elif source == 'Booking':
                        url = urls.booking_url
                        if url:
                            main_dict['Booking'] = scrape_booking(driver, url)
                        else:
                            main_dict['Booking'] = {"Error": "URL not found"}
                    else:
                        main_dict[source] = {}
                    time.sleep(40)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            
            def create_partner_rating(partner_name, ratings):
                    if not isinstance(ratings, dict):
                        print(f"Skipping {partner_name} due to invalid data format.")
                        return
                    if partner_name=='MakeMyTrip':
                        room= float(ratings.get('Amenities', 0) or 0)
                        service=float(ratings.get('Hospitality', 0) or 0)
                        value= float(ratings.get('Value For Money', 0) or 0)
                    else:
                        room=float(ratings.get('Comfort', 0) or 0)
                        service=float(ratings.get('Staff', 0) or 0)
                        value= float(ratings.get('Value for money', 0) or 0)
                    PartnerRating.objects.create(
                        partner_type=partner_name,
                        OrganizationID=OrganizationID,
                        overall_rating=float(ratings.get('Overall Rating', 0) or 0),
                        cleanliness=float(ratings.get('Cleanliness', 0) or 0),
                        location= float(ratings.get('Location', 0) or 0),
                        service= service,  
                        room= room,  
                        value= value, 
                        facilities=float(ratings.get('Facilities', 0) or 0),
                        food=float(ratings.get('Food', 0) or 0),
                        wifi= float(ratings.get('Free WiFi', 0) or 0),
                        
                    )

            def process_data(data):
                for partner_name, ratings in data.items():
                    if partner_name == 'Error':
                        print(f"Error encountered: {ratings}")
                        continue
                    if isinstance(ratings, dict):
                        create_partner_rating(partner_name, ratings)
                    else:
                        print(f"Skipping {partner_name} due to unexpected data format.")
            process_data(main_dict)
        else: 
            continue
    
    driver.quit()