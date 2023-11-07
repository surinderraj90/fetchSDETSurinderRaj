from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Step 1: Launch the website
url = "http://sdetchallenge.fetch.com/"  # Replace with the actual URL
driver = webdriver.Chrome()  # Change to your preferred browser driver
driver.get(url)

# Step 2: Define a function to perform a weighing
def perform_weighing_1(left, right):
    left_bowl_0 = driver.find_element(By.XPATH, "//*[@id='left_0']")
    right_bowl_0 = driver.find_element(By.XPATH, "//*[@id='right_0']")
    left_bowl_1 = driver.find_element(By.XPATH, "//*[@id='left_1']")
    right_bowl_1 = driver.find_element(By.XPATH, "//*[@id='right_1']")
    left_bowl_2 = driver.find_element(By.XPATH, "//*[@id='left_2']")
    right_bowl_2 = driver.find_element(By.XPATH, "//*[@id='right_2']")
    weigh_button = driver.find_element(By.ID, "weigh")
    reset_button = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[4]/button[1]")
    left_bowl_0.clear()
    right_bowl_0.clear()
    left_bowl_1.clear()
    right_bowl_1.clear()
    left_bowl_2.clear()
    right_bowl_2.clear()
    left_bowl_0.send_keys(left[0])
    right_bowl_0.send_keys(right[0])
    left_bowl_1.send_keys(left[1])
    right_bowl_1.send_keys(right[1])
    left_bowl_2.send_keys(left[2])
    right_bowl_2.send_keys(right[2])
    weigh_button.click()

    # Wait for the result to appear
    time.sleep(15)
    weighing_list = driver.find_element(By.CSS_SELECTOR, '.game-info ol')
    last_weighing = weighing_list.find_elements(By.TAG_NAME, 'li')[-1]
    result = last_weighing.text
    reset_button.click()
    return result

def perform_weighing_2(left_1, right_1):
    left_bowl_0_1 = driver.find_element(By.XPATH, "//*[@id='left_0']")
    right_bowl_0_1 = driver.find_element(By.XPATH, "//*[@id='right_0']")
    left_bowl_1_1 = driver.find_element(By.XPATH, "//*[@id='left_1']")
    right_bowl_1_1 = driver.find_element(By.XPATH, "//*[@id='right_1']")
    left_bowl_2_1 = driver.find_element(By.XPATH, "//*[@id='left_2']")
    right_bowl_2_1 = driver.find_element(By.XPATH, "//*[@id='right_2']")
    weigh_button_1 = driver.find_element(By.ID, "weigh")
    left_bowl_0_1.send_keys(left_1)
    right_bowl_0_1.send_keys(right_1)
    weigh_button_1.click()

    # Wait for the result to appear
    time.sleep(15)
    weighing_list_1 = driver.find_element(By.CSS_SELECTOR, '.game-info ol')
    last_weighing_1 = weighing_list_1.find_elements(By.TAG_NAME, 'li')[-1]
    result = last_weighing_1.text
    return result

# Step 3: Implement the algorithm to find the fake gold bar
def find_fake_gold_bar():
    weighings = []
    while True:
        # Divide bars into three groups
        left_group = [0, 1, 2]
        right_group = [3, 4, 5]

        # Perform the initial weighing
        result_1 = perform_weighing_1(left_group, right_group)


        if "=" in result_1:
            # The fake bar is in one of the three remaining bars (6, 7, 8)
            left_group_1 = 6
            right_group_1 = 7
            result_2 = perform_weighing_2(left_group_1, right_group_1)

            if "=" in result_2:
                fake_bar = 8
            elif ">" in result_2:
                fake_bar = 7
            else:
                fake_bar = 6

        elif ">" in result_1:
            left_group_1 = 3
            right_group_1 = 4
            result_2 = perform_weighing_2(left_group_1, right_group_1)

            if "=" in result_2:
                fake_bar = 4
            elif ">" in result_2:
                fake_bar = 4
            else:
                fake_bar = 3

        else:

            # The fake bar is in the left group
            left_group_1 = 0
            right_group_1 = 1
            result_2 = perform_weighing_2(left_group_1, right_group_1)

            if "=" in result_2:
                fake_bar = 3
            elif ">" in result_2:
                fake_bar = 1
            else:
                fake_bar = 0

        # Perform the second weighing
        return fake_bar

# Step 4: Identify the fake gold bar and click on it
fake_bar_number = find_fake_gold_bar()
coin_bar = "coin_" + str(fake_bar_number)
fake_bar_button = driver.find_element(By.XPATH, f"//*[@id='{coin_bar}']")
fake_bar_button.click()

# Step 5: Capture the alert message
alert = driver.switch_to.alert
alert_message = alert.text
if "Yay" in alert_message:
    print(f"We have found the correct fake bar")
    print(f"Fake Gold Bar: {fake_bar_number}")
alert.accept()

# Step 6: Output the results
# print(f"Fake Gold Bar: {fake_bar_number}")

# Close the web browser
driver.quit()