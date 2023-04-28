from keras.models import load_model  
from PIL import Image, ImageOps  
import numpy as np
import streamlit as st
import streamlit.components.v1 as com
from PIL import Image
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import keyboard
import os
import webbrowser
import base64

image_file = 'kitchen-7870212.jpg'

with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

st.title('Recipe Genie Pad')
st.write('$$Your$$ $$Wish$$ $$Is$$ $$My$$ $$Command$$ **😋**')
np.set_printoptions(suppress=True)
# Load the model
model = load_model("model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()


data = np.ndarray(shape=(1, 299, 299, 3), dtype=np.float32)
# Upload the Image for model
uploaded_file = st.file_uploader('Upload an Image of your $$Desired$$ $$Dish$$')
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image,caption='Uploaded Dish')
    # resizing the image to 299x299 
    size = (299, 299)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    foodname = class_name[2:].strip()
    # Display the predicted Dish Name with Confidence Score
    st.write(f'The Prediction is: $${foodname}$$')
    st.write(f'Confidence %:', (confidence_score*100).round(3))
    # Useing Webscrap url to open the links
    youtube_url = f"https://www.youtube.com/results?search_query=how+to+make+{foodname}"
    blog_url = f"https://www.bbcgoodfood.com/search?q={foodname}"
    
    
    st.header(f'Checkout how to make {foodname} :')
    col11, col12 = st.columns(2)
    with col11:
        st.write(f'Video')
        if st.button(f'Youtube'):
            webbrowser.open(youtube_url)

    with col12:
        st.write(f'Blog')
        if st.button(f'Blog'):
            webbrowser.open(blog_url)
        
    st.header(f"$$Not$$ in mood to $$Cook$$,")
    st.write(f"**Don't worry we got you Bro!**")
    if st.button(f'Order $${foodname}$$ now!'):
        # Launch the Chrome browser and navigate to Swiggy
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        driver.get("https://www.swiggy.com/")
        # Wait for the page to load
        time.sleep(5)
        # Click on the "Locate Me" button
        locate_button = driver.find_element(By.CLASS_NAME, "_1fiQt")
        locate_button.click()
        # Wait for the location to be detected
        time.sleep(5)
        # Get the current URL and append /search to it
        current_url = driver.current_url
        search_url = current_url + f"search?query={foodname}"
        driver.get(search_url)
        # Prompt the user to input ` to close the browser
        keyboard.wait("`")
        driver.quit()

            

    st.header(f'Ordered In $$Excess$$? Need to Throw it out!!!')
    st.write(f'**$$Donate$$** Today and $$Save$$ $$Lives$$!')
    st.write("Wastage for you is one time meal for someone else.")
    if st.button(f'Donate Leftover Food!'):
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
        # Navigate to Google
        driver.get("https://www.google.com")

        # Find the search box and enter a query
        search_box = driver.find_element(By.NAME, 'q')
        search_box.send_keys("ngo for food donation near me")
        search_box.send_keys(Keys.RETURN)

        # Wait for the results to load
        time.sleep(10)

        search_result = driver.find_element(By.CSS_SELECTOR, "a.yYlJEf.Q7PwXb.L48Cpd.brKmxb")

        # Get the href attribute value of the link element
        href = search_result.get_attribute("href")

        # Open the href in a new tab
        driver.execute_script("window.open('"+href+"', '_blank')")

        # Prompt the user to input ` to close the browser
        keyboard.wait("`")
        driver.quit()
    # Tells on different ways to save food
    st.write("Here are some ways to **Save** **Food**:")

    st.write("- Plan your meals ahead of time to avoid buying too much food")
    st.write("- Store food properly to keep it fresh longer, such as using airtight containers or wrapping it tightly in plastic wrap")
    st.write("- Freeze leftover food for future use")
    st.write("- Use wilted vegetables or fruits in soups or smoothies")
    st.write("- Make use of leftovers in new dishes, such as using leftover rice to make fried rice")
    st.write("- Donate excess food to a food bank or shelter")
    st.write("- Compost food scraps to reduce waste")
    
    st.write("By following these tips, we can help reduce food waste and make the most of the food we have.") 
