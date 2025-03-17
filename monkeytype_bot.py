import string
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
import time
import random

driver = webdriver.Chrome()

def close_cookie():
    closed = False
    while not closed:
        try:
            driver.find_element(By.CLASS_NAME, "rejectAll").click()
            print('Cookie closed')
        except NoSuchElementException:
            time.sleep(0.5)
        else:
            closed = True

try:
    # set error percentage | uncomment to request for error percentage on start
    # error = int(input('Set error percentage (4%): ').replace('%', '').replace('', '4'))
    error = 4

    driver.get("https://monkeytype.com")
    print('Page is loading...')
    time.sleep(1)

    close_cookie()
    driver.find_element(By.TAG_NAME, "body").click()  # focus on body
    time.sleep(1)

    # Change typing time to 15 secs
    print('Changing time to 15 secs')
    driver.find_element(By.CLASS_NAME, "time").find_elements(By.TAG_NAME, "button")[0].click()
    time.sleep(1)

    words = driver.find_element(By.ID, "words")
    all_words = words.find_elements(By.CLASS_NAME, "word")

    total_errors = (error/100) * len(all_words)

    errors_made = 0
    print('Bot is starting...')
    for word in all_words:
        letters = word.find_elements(By.TAG_NAME, "letter")
        if errors_made < total_errors:
            # time to sieve-in some errors
            random_char = random.choice(string.ascii_letters)
            word_text = "".join([letter.text for letter in letters[:len(letters) - 2]]) + random_char
            errors_made += 1
        else:
            word_text = "".join([letter.text for letter in letters])
        driver.switch_to.active_element.send_keys(word_text + " ")
        time.sleep(0.1)  # our typing speed, adjust to liking

    print("Typing completed successfully!")

except StaleElementReferenceException as e:
    print("typing has ended.")

except Exception as e:
    print("Error: " + str(e))

finally:
    if input("Press Enter to exit...") == "":
        driver.quit()
