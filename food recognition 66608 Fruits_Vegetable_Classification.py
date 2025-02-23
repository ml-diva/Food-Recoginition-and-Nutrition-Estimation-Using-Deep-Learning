import streamlit as st
from PIL import Image
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup

model = load_model('FV.h5')
labels = {0: 'apple', 1: 'banana', 2: 'beetroot', 3: 'bell pepper', 4: 'cabbage', 5: 'capsicum', 6: 'carrot',
          7: 'cauliflower', 8: 'chilli pepper', 9: 'corn', 10: 'cucumber', 11: 'eggplant', 12: 'garlic', 13: 'ginger',
          14: 'grapes', 15: 'jalepeno', 16: 'kiwi', 17: 'lemon', 18: 'lettuce',
          19: 'mango', 20: 'onion', 21: 'orange', 22: 'paprika', 23: 'pear', 24: 'peas', 25: 'pineapple',
          26: 'pomegranate', 27: 'potato', 28: 'raddish', 29: 'soy beans', 30: 'spinach', 31: 'sweetcorn',
          32: 'sweetpotato', 33: 'tomato', 34: 'turnip', 35: 'watermelon'}

fruits = ['Apple', 'Banana', 'Bello Pepper', 'Chilli Pepper', 'Grapes', 'Jalepeno', 'Kiwi', 'Lemon', 'Mango', 'Orange',
          'Paprika', 'Pear', 'Pineapple', 'Pomegranate', 'Watermelon']
vegetables = ['Beetroot', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Corn', 'Cucumber', 'Eggplant', 'Ginger',
              'Lettuce', 'Onion', 'Peas', 'Potato', 'Raddish', 'Soy Beans', 'Spinach', 'Sweetcorn', 'Sweetpotato',
              'Tomato', 'Turnip']




def fetch_calories(prediction):
    try:
        url = 'https://www.google.com/search?&q=calories in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        calories = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return calories
    except Exception as e:
        st.error("Can't able to fetch the Calories")
        print(e)


def fetch_protein(prediction):
    try:
        url = 'https://www.google.com/search?q=protein in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        protein = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return protein
    except Exception as e:
        st.error("Can't able to fetch the protein")
        print(e)
def fetch_carbohydrates(prediction):
    try:
        url = 'https://www.google.com/search?q=carbohydrates in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        carbohydrates = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return carbohydrates
    except Exception as e:
        st.error("Can't able to fetch the Carbohydrates")
        print(e)
def fetch_fats(prediction):
    try:
        url = 'https://www.google.com/search?q=fats in ' + prediction
        req = requests.get(url).text
        scrap = BeautifulSoup(req, 'html.parser')
        fats = scrap.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return fats
    except Exception as e:
        st.error("Can't able to fetch the Fats")
        print(e)

def processed_img(img_path):
    img = load_img(img_path, target_size=(224, 224, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    return res.capitalize()


def run():
    st.title("🥘Food Recognition and Nutrition Estimation🍔")
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, use_column_width=False)
        save_image_path = '/Users/Devi Anuhya/Desktop/myproject/6608/output/' + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result = processed_img(save_image_path)
            print(result)
            if result in vegetables:
                st.info('**Category : Vegetables**')
            else:
                st.info('**Category : Fruit**')
            st.success("**Predicted : " + result + '**')
            cal = fetch_calories(result)
            if cal:
                st.warning('**' + cal + '(100 grams)**')
            pro = fetch_protein(result)
            if pro:
                st.warning('**' + pro + ' Proteins (100 grams)**')
            carb = fetch_carbohydrates(result)
            if carb:
                st.warning('**' + carb + ' Carbohydrates (100 grams)**')
            fat = fetch_fats(result)
            if fat:
                st.warning('**' + fat + ' Fats (100 grams)**')
    
    

    st.write("**Let's check your BMI ↓**")
    weight = st.number_input("Enter your weight (in kg)")
    height = st.number_input("Enter your height (in meter)")

    if(st.button('Calculate BMI')) :
        bmi = weight / (height ** 2)

        st.text("Your BMI index is {}.".format(bmi))

        if(bmi < 16):
          st.error("You are Extremely Underweight")
          st.toast('Add extra calories to your meals and doing some exercise to increase your appetite!', icon='🥙')
        elif(bmi >= 16 and bmi < 18.5):
          st.warning("You are Underweight")
          st.toast('Eat more high-calorie food!', icon='🥩')
        elif(bmi >= 18.5 and bmi < 25):
          st.success("You are Healthy , Please maintain the same c")
          st.balloons()
        elif(bmi >= 25 and bmi < (31-1)):
          st.warning("You are Overweight")
          st.toast('Eat more healthy food and maintain calorie deficit!', icon='🍎')
        elif(bmi >= (31-1)):
          st.error("You are Extremely Overweight")
          st.toast('Eat a balanced and do some diet!', icon='💪')

run()
