from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import itertools
import pandas as pd
 
url = "https://www.nal.usda.gov/human-nutrition-and-food-safety/dri-calculator"

driver = webdriver.Chrome()
driver.get(url)
print(f"{driver.title} Mounted successfully!")


# Variables
data = [] 

sex_options= ['edit-sex-male','edit-sex-female']
age_range = range(18, 20)
height_ft_range = [5, 6]
height_in_range = [0, 6]
weight_kg_range = range(75, 125)

# Generate all combinations of random values
combinations = list(itertools.product(sex_options, age_range, height_ft_range, height_in_range, weight_kg_range))
print(f"Total combinations: {len(combinations)}")
print(f"Expected to take: {len(combinations)*4/60} minutes or {len(combinations)*4/60/60} hours")
# Loop over the combinations
print("Extracting data...")
for combination in combinations:
    # Gets the values
    sex_option, age, height_ft, height_in, weight_kg = combination
    radio_button_sex = driver.find_element(By.CSS_SELECTOR, f"label[for='{sex_option}']")
    dropdown_pregnant = driver.find_element(By.CSS_SELECTOR, "option[value=none]")
    dropdown_input_activity = driver.find_element(By.ID, "edit-activity-level")
    radio_button_metric = driver.find_element(By.ID, "edit-measurement-units-met")
    num_input_age = driver.find_element(By.ID, "edit-age-value")
    dropdown_input_preg = driver.find_element(By.ID, "edit-pregnancy-lactating")
    num_input_height_cm = driver.find_element(By.ID, "edit-cm")
    num_input_height_ft = driver.find_element(By.ID, "edit-feet")
    num_input_height_in = driver.find_element(By.ID, "edit-inches")
    num_input_weight_kg = driver.find_element(By.ID, "edit-kilos")
    num_input_weight_lb = driver.find_element(By.ID, "edit-pounds")
    dropdown_input_activity = driver.find_element(By.ID, "edit-activity-level")
    submit_button = driver.find_element(By.ID, "edit-submit")
    dropdown_options = driver.find_element(By.CSS_SELECTOR, "option[value=Sedentary]")
    try:
        radio_button_sex.click()
        num_input_age.click()
        num_input_age.send_keys(age)
        num_input_height_ft.click()
        num_input_height_ft.send_keys(height_ft)
        num_input_height_in.click()
        num_input_height_in.send_keys(height_in)
        num_input_weight_lb.click()
        num_input_weight_lb.send_keys(round(weight_kg*2.205, 0))
        dropdown_input_activity.click()
        dropdown_options.click()
        if sex_option == 'edit-sex-female':
            dropdown_input_preg.click()
            dropdown_pregnant.click()
    except ElementClickInterceptedException as e:
        no_thanks_id = driver.find_element(By.ID, "cfi_btnNoThanks")
        no_thanks_id.click()
        radio_button_sex.click()
        num_input_age.click()
        num_input_age.clear()
        num_input_age.send_keys(age)
        num_input_height_ft.click()
        num_input_height_ft.clear()
        num_input_height_ft.send_keys(height_ft)
        num_input_height_in.click()
        num_input_height_in.clear()
        num_input_height_in.send_keys(height_in)
        num_input_weight_lb.click()
        num_input_weight_lb.clear()
        num_input_weight_lb.send_keys(round(weight_kg*2.205, 0))
        dropdown_input_activity.click()
        dropdown_options.click()
        if sex_option == 'edit-sex-female':
            dropdown_input_preg.click()
            dropdown_pregnant.click()
    # Submit and wait for the DOM to load
    submit_button.click()
    driver.implicitly_wait(3)
    # Extract the data from the tables
    data_sex = driver.find_element(By.CSS_SELECTOR, "td[headers='sex']").text
    data_age = driver.find_element(By.CSS_SELECTOR, "td[headers='age']").text
    data_height = driver.find_element(By.CSS_SELECTOR, "td[headers='height']").text
    data_weight = driver.find_element(By.CSS_SELECTOR, "td[headers='weight']").text
    data_activity_level = driver.find_element(By.CSS_SELECTOR, "td[headers='activity-level']").text
    data_bmi = driver.find_element(By.CSS_SELECTOR, "td[headers='bmi']").text
    data_daily_calories = driver.find_element(By.CSS_SELECTOR, "td[headers='eer']").text
    data_fiber = driver.find_element(By.CSS_SELECTOR, "td[headers='total-fiber macro-recommended-intake']").text
    data_protein = driver.find_element(By.CSS_SELECTOR, "td[headers='protein macro-recommended-intake']").text
    data_vitamin_c = driver.find_element(By.CSS_SELECTOR, "td[headers='vitamin-c vitamin-recommended-intake']").text
    data_vitamin_a = driver.find_element(By.CSS_SELECTOR, "td[headers='vitamin-a vitamin-recommended-intake']").text
    data_vitamin_d = driver.find_element(By.CSS_SELECTOR, "td[headers='vitamin-d vitamin-recommended-intake']").text
    data_vitamin_e = driver.find_element(By.CSS_SELECTOR, "td[headers='vitamin-e vitamin-recommended-intake']").text
    data_vitamin_b12 = driver.find_element(By.CSS_SELECTOR, "td[headers='vitamin-b<sub>12</sub> vitamin-recommended-intake']").text
    data_vitamin_k = driver.find_element(By.CSS_SELECTOR, "td[headers='vitamin-k vitamin-recommended-intake']").text
    data_niacin = driver.find_element(By.CSS_SELECTOR, "td[headers='niacin vitamin-recommended-intake']").text
    data_calcium = driver.find_element(By.CSS_SELECTOR, "td[headers='calcium mineral-recommended-intake essential']").text
    data_carbs = driver.find_element(By.CSS_SELECTOR, "td[headers='carbohydrate macro-recommended-intake']")
    data_water = driver.find_element(By.CSS_SELECTOR, "td[headers='total-water macro-recommended-intake']")
    data_fat = driver.find_element(By.CSS_SELECTOR, "td[headers='fat macro-recommended-intake']")

    # This is the output of the csv without the code I added below. There is additional text of another element and it's easier to remove it now than preprocessing later.
    ##################################################################################################
    # Male,18 years,4 ft. 0 in.,88 lbs.,Sedentary,26.9,"1,166 kcal/day","131 - 189 grams             #
    # More Information About Carbohydrate",38 grams,34 grams,"32 - 45 grams                          #
    # More Information About Fat","3.3 liters (about 14 cups)                                        #
    # More Information About Water",75 mg,900 mcg,15 mcg,15 mg,2.4 mcg,75 mcg,16 mg,"1,300 mg"       #
    ##################################################################################################
    for child_element in data_carbs.find_elements(By.CSS_SELECTOR, 'a'):
        data_carbs = data_carbs.text.replace(child_element.text, '')
    for child_element in data_fat.find_elements(By.CSS_SELECTOR, 'a'):
        data_fat = data_fat.text.replace(child_element.text, '')
    for child_element in data_water.find_elements(By.CSS_SELECTOR, 'a'):
        data_water = data_water.text.replace(child_element.text, '')
    # Combine all variables into one array
    csv_data = [data_sex, data_age, data_height, data_weight, data_activity_level, data_bmi,
                data_daily_calories, data_carbs, data_fiber, data_protein, data_fat,
                data_water, data_vitamin_c, data_vitamin_a, data_vitamin_d, data_vitamin_e,
                data_vitamin_b12, data_vitamin_k, data_niacin, data_calcium]
    # And then append it to the global array
    data.append(csv_data)
    
    # Go back to the calculator page
    driver.get(url)
# Get the column names and create a dataframe
columns = ["Sex", "Age", "Height", "Weight", "Activity Level", "BMI", "Daily Calories", "Carbs", "Fiber", "Protein", "Fat", "Water", "Vitamin C", "Vitamin A", "Vitamin D", "Vitamin E", "Vitamin B12", "Vitamin K", "Niacin", "Calcium"]
df = pd.DataFrame(data=data,columns=columns)
print("Saving data...")
df.to_csv("recommended_nutrition_full.csv", index=False)
print("Data saved!")
driver.quit()