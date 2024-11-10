import os
import pandas as pd
import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
from googletrans import Translator  # Import Translator for Google Translate

# Initialize the Translator object for Google Translate
translator = Translator()

# Load data from Excel file for offline mode
data = pd.read_excel("pak.xlsx")

# Simulated offline response using the Excel data
def get_offline_response(query):
    # Search the Excel data for the best response
    for _, row in data.iterrows():
        if query.lower() in str(row['Description']).lower():
            return f"Offline mode: {row['Description']}"
    return "Offline mode: Information not available for your query."

# Groq API settings with corrected endpoint URL
GROQ_API_KEY = "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"  # Replace with your API Key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Check if this is the correct URL

# Streamlit UI for the chatbot
st.markdown("""<style>
body {
    background-color: #f0f8ff;
    font-family: 'Arial', sans-serif;
}
.stButton button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    cursor: pointer;
    border-radius: 12px;
}
.stButton button:hover {
    background-color: #45a049;
}
.stTextInput input {
    border-radius: 10px;
    padding: 10px;
    border: 2px solid #4CAF50;
    width: 100%;
}
h1 {
    color: #4CAF50;
}
h2 {
    color: #4CAF50;
}
p {
    color: #333333;
}
</style>""", unsafe_allow_html=True)

# Greeting and initial introduction
st.title("DiscoverPak - Virtual Pakistan Travel Guide")
st.subheader("Your friendly virtual tour guide with 40 years of expertise in Pakistan's travel spots.")
st.write("Welcome! You can ask me about famous places, weather, events, or other travel-related topics in Pakistan.")

# Help dropdown with detailed features
with st.expander("Help", expanded=False):
    st.write("### Welcome to DiscoverPak!")
    st.write("This chatbot can assist you with the following features:")
    st.write("1. **Travel Information:** Get detailed information about famous travel destinations.")
    st.write("2. **Directions:** Guidance to reach various locations with travel tips.")
    st.write("3. **Weather Updates:** Current weather information for regions.")
    st.write("4. **Local Events:** Information on upcoming events and activities.")
    st.write("5. **Travel Tips:** Advice on safety, cultural etiquette, and more.")
    st.write("6. **Feedback and Queries:** Share your feedback or ask additional questions.")

# Text input for the user query
user_input = st.text_input("Type your question here", key="query")

# Button to submit the query and handle response
if st.button("Submit Query") or user_input:
    if user_input:
        try:
            # Request payload for the Groq API
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
            payload = {
                "messages": [{"role": "user", "content": user_input}],
                "model": "llama3-8b-8192"
            }

            # Make the API call directly with requests
            response = requests.post(GROQ_API_URL, headers=headers, json=payload)

            # Check for 404 and log the error
            if response.status_code != 200:
                st.error(f"Error: {response.status_code}, {response.text}")
            
            response.raise_for_status()  # Raise error if status is not 200
            
            # Parse the API response
            response_json = response.json()
            if 'choices' in response_json and len(response_json['choices']) > 0:
                response_text = response_json['choices'][0]['message']['content']
                st.write("Chatbot response (DiscoverPak):")
                st.write(response_text)

                # Translate the response text into Urdu
                translated_text = translator.translate(response_text, src='en', dest='ur').text
                st.write("Chatbot response (in Urdu - DiscoverPak):")
                st.write(translated_text)

            else:
                st.error("Unexpected API response format. Please check the response structure.")
        except requests.exceptions.RequestException:
            # Fallback to offline mode response
            response_text = get_offline_response(user_input)
            st.write(response_text)

            # Translate the offline response into Urdu
            translated_text = translator.translate(response_text, src='en', dest='ur').text
            st.write("Offline response (in Urdu - DiscoverPak):")
            st.write(translated_text)

# Map feature
st.subheader("Explore Tourist Locations on the Map")
map = folium.Map(location=[30.3753, 69.3451], zoom_start=5)  # Centered on Pakistan



tourist_locations = [
    {"name": "Walled City", "coordinates": [31.588126, 74.30932246]},
    {"name": "Shigar District", "coordinates": [35.7106418, 76.55314235]},
    {"name": "Bourbon", "coordinates": [33.9550872, 73.4518727]},
    {"name": "Talhaar", "coordinates": [33.7742831, 73.1139125]},
    {"name": "Karakoram", "coordinates": [35.7416218, 76.5118925]},
    {"name": "Skardu", "coordinates": [34.9565886, 75.47983135]},
    {"name": "Derawar", "coordinates": [28.76800705, 71.33424735]},
    {"name": "Dhani", "coordinates": [34.4241, 73.6911]},
    {"name": "Walled City", "coordinates": [31.588126, 74.30932246]},
    {"name": "Tato", "coordinates": [35.3872034, 74.57892916]},
    {"name": "Islamabad", "coordinates": [33.7297492, 73.03736]},
    {"name": "Skardu", "coordinates": [35.9995, 75.9999]},
    {"name": "Jiwani Tehsil", "coordinates": [25.154342, 62.0499838]},
    {"name": "Gojal", "coordinates": [36.6176353, 74.8632045]},
    {"name": "Bagrote", "coordinates": [26.8611674, 67.1511368]},
    {"name": "Kotli", "coordinates": [33.46410685, 73.86825122]},
    {"name": "Gawadar", "coordinates": [25.5064168, 65.530701]},
    {"name": "Garelth", "coordinates": [36.3167, 74.65]},
    {"name": "Banda-i-Sazin", "coordinates": [35.5074167, 73.2877772]},
    {"name": "Kumrat Valley", "coordinates": [35.5638686, 72.1941226]},
    {"name": "Kalam Tehsil", "coordinates": [35.4902, 72.5796]},
    {"name": "Chitral Tehsil", "coordinates": [35.6838, 71.6554]},
    {"name": "Khabeki", "coordinates": [32.6774124, 72.2474823]},
    {"name": "Broghil Valley", "coordinates": [36.8784107, 73.70117513]},
    {"name": "Choa Saidan Shah", "coordinates": [32.7239451, 72.9516404]},
    {"name": "Khewra", "coordinates": [32.6465569, 73.0062054]},
    {"name": "Kaghan", "coordinates": [34.77916173, 73.52379989]},
    {"name": "Walled City", "coordinates": [31.58803305, 74.31495649]},
    {"name": "Kaghan", "coordinates": [34.8818168, 73.6957232]},
    {"name": "Gadani", "coordinates": [25.1186, 66.7267]},
    {"name": "Kalam Tehsil", "coordinates": [35.7139, 72.651]},
    {"name": "Malum Jabba", "coordinates": [34.7999, 72.5722]},
    {"name": "Sadhupur Rhok", "coordinates": [35.066229, 75.9947968]},
    {"name": "Walled City", "coordinates": [31.5833, 74.3236]},
    {"name": "Kalam Tehsil", "coordinates": [35.5418, 72.6595]},
    {"name": "Lahore", "coordinates": [31.5925, 74.3095]},
    {"name": "Karachi Division", "coordinates": [24.8142, 67.033]},
    {"name": "Balhrejee", "coordinates": [27.3243, 68.1357]},
    {"name": "Khuzdar", "coordinates": [27.7572, 66.6405599]},
    {"name": "Naltar Valley", "coordinates": [36.2397, 74.0821]},
    {"name": "Rawalpindi", "coordinates": [33.683958, 73.5289869]},
    {"name": "Mori Syedan", "coordinates": [33.66149, 73.384519]},
    {"name": "Athmuqam Tehsil", "coordinates": [34.5985, 73.9073]},
    {"name": "Sari Bang", "coordinates": [33.893504, 73.117348]},
    {"name": "Karachi Division", "coordinates": [24.8709, 67.0961]},
    {"name": "Islamabad", "coordinates": [33.6931, 73.0689]},
    {"name": "Islamabad", "coordinates": [33.7332, 73.5325]},
    {"name": "Pattan", "coordinates": [35.11235, 73.005843]},
    {"name": "Islamabad", "coordinates": [33.787, 73.1084]},
    {"name": "Rama", "coordinates": [35.3303, 74.7856]},
    {"name": "Athmuqam Tehsil", "coordinates": [34.8296, 74.0625]},
    {"name": "Rawalakot", "coordinates": [33.8584, 73.7654]},
    {"name": "Rohtas", "coordinates": [32.9645, 73.5745]},
    {"name": "Naar Valley", "coordinates": [36.1745, 74.8825]},
    {"name": "Sajikot", "coordinates": [34.001104, 73.278766]},
    {"name": "Milpin", "coordinates": [35.2294, 75.6295]},
    {"name": "Begampura", "coordinates": [31.5843, 74.3828]},
    {"name": "Kachura", "coordinates": [35.4275, 75.4567]},
    {"name": "Mansehra", "coordinates": [33.7773, 73.17057]},
    {"name": "Gamba", "coordinates": [35.3247, 75.551]},
    {"name": "Karachi Division", "coordinates": [24.89951, 66.96973]},
    {"name": "Taxila", "coordinates": [33.7459, 72.8187]},
    {"name": "Bhakkar", "coordinates": [31.2281, 71.8099]},
    {"name": "Lahore", "coordinates": [31.5684, 74.3081]},
    {"name": "Phagwari", "coordinates": [33.97709, 73.48238]},
    {"name": "Gwādar", "coordinates": [25.1594, 62.1816]},
    {"name": "Karachi", "coordinates": [24.8474, 67.0329]},
    {"name": "Karachi", "coordinates": [24.78, 67.04]},
    {"name": "Karachi", "coordinates": [24.8625, 67.0295]},
    {"name": "Karachi", "coordinates": [24.47386, 66.58391]},
    {"name": "Karachi", "coordinates": [40.7586, 73.9762]},
    {"name": "Karachi", "coordinates": [24.8754, 67.041]},
    {"name": "Karachi", "coordinates": [24.8644, 67.2714]},
    {"name": "Karachi", "coordinates": [24.8143, 67.0327]},
    {"name": "Islamabad", "coordinates": [33.7296, 73.0368]},
    {"name": "Islamabad", "coordinates": [33.7383, 73.0565]},
    {"name": "Islamabad", "coordinates": [33.6933, 73.0682]},
    {"name": "Islamabad", "coordinates": [33.6885, 73.0727]},
    {"name": "Islamabad", "coordinates": [33.7027, 73.1261]},
    {"name": "Islamabad", "coordinates": [33.7481, 73.0051]},
    {"name": "Islamabad", "coordinates": [33.7427, 73.0678]},
    {"name": "Islamabad", "coordinates": [33.6887, 73.0887]},
    {"name": "Islamabad", "coordinates": [33.7077, 73.0498]},
    {"name": "Islamabad", "coordinates": [33.7015, 73.0884]},
    {"name": "Lahore", "coordinates": [74.3175, 31.5889]},
    {"name": "Lahore", "coordinates": [74.3093, 31.5884]},
    {"name": "Lahore", "coordinates": [74.3791, 31.5816]},
    {"name": "Lahore", "coordinates": [74.308, 31.5925]},
    {"name": "Lahore", "coordinates": [74.3159, 31.5707]},
    {"name": "Lahore", "coordinates": [74.3137, 31.5831]},
    {"name": "Lahore", "coordinates": [74.3111, 31.5706]},
    {"name": "Lahore", "coordinates": [74.3157, 31.5784]},
    {"name": "Lahore", "coordinates": [74.3361, 31.5312]},
    {"name": "Lahore", "coordinates": [74.3176, 31.5892]},
    {"name": "Lahore", "coordinates": [74.3406, 31.545]},
    {"name": "Lahore", "coordinates": [74.3013, 31.6222]},
    {"name": "Lahore", "coordinates": [74.3174, 31.6214]},
    {"name": "Lahore", "coordinates": [74.315, 31.59]},
    {"name": "Lahore", "coordinates": [74.3727, 31.5035]},
    {"name": "Lahore", "coordinates": [74.3588, 31.5132]},
    {"name": "Lahore", "coordinates": [74.3411, 31.4548]},
    {"name": "Lahore", "coordinates": [74.2546, 31.4758]},
    {"name": "Lahore", "coordinates": [74.3162, 31.5497]},
    {"name": "Lahore", "coordinates": [74.3527, 31.5195]},
    {"name": "Hunza", "coordinates": [36.3167, 74.65]},
    {"name": "Chilas", "coordinates": [35.3965, 74.6973]},
    {"name": "Gilgit", "coordinates": [36.0654, 74.3514]},
    {"name": "Skardu", "coordinates": [35.3351, 75.5594]},
    {"name": "Naran", "coordinates": [34.876, 73.6987]},
    {"name": "Chitral", "coordinates": [36.0782, 72.6084]},
    {"name": "Passu", "coordinates": [36.4693, 74.8915]},
    {"name": "Sost", "coordinates": [36.85, 75.4573]},
    {"name": "Muzaffarabad", "coordinates": [34.8231, 74.2915]},
    {"name": "Skardu", "coordinates": [35.0076, 75.2875]},
    {"name": "Astore", "coordinates": [35.3657, 74.7973]},
    {"name": "Hunza", "coordinates": [36.3309, 74.857]},
    {"name": "Gilgit", "coordinates": [35.9635, 74.38]},
    {"name": "Skardu", "coordinates": [35.3333, 75.5667]},
    {"name": "Skardu", "coordinates": [35.4423, 75.4849]},
    {"name": "Peshawar", "coordinates": [33.7901, 72.3277]},
    {"name": "Peshawar", "coordinates": [36.4333, 72.6667]},
    {"name": "Peshawar", "coordinates": [36.2833, 72.5167]},
    {"name": "Peshawar", "coordinates": [24.0944, 67.4389]},
    {"name": "Peshawar", "coordinates": [36.0075, 71.7578]},
    {"name": "Peshawar", "coordinates": [36.0075, 71.7578]},
    {"name": "Peshawar", "coordinates": [33.6624, 71.8374]},
    {"name": "Peshawar", "coordinates": [34.0056, 71.5639]},
    {"name": "Peshawar", "coordinates": [34.0072, 71.5728]},
    {"name": "Peshawar", "coordinates": [34.015, 71.5747]},
    {"name": "Peshawar", "coordinates": [34.0238, 71.5691]},
    {"name": "Peshawar", "coordinates": [34.0143, 71.5713]},
    {"name": "Peshawar", "coordinates": [34.0056, 71.5639]},
    {"name": "Peshawar", "coordinates": [34.0072, 71.5728]},
    {"name": "Peshawar", "coordinates": [34.015, 71.5747]},
    {"name": "Peshawar", "coordinates": [34.0238, 71.5691]},
    {"name": "Peshawar", "coordinates": [34.0143, 71.5713]},
    {"name": "Peshawar", "coordinates": [34.0061, 71.5576]},
    {"name": "Peshawar", "coordinates": [34.0123, 71.5801]},
    {"name": "Peshawar", "coordinates": [34.0085, 71.5742]},
    {"name": "Peshawar", "coordinates": [34.0125, 71.578]},
    {"name": "Peshawar", "coordinates": [34.019, 71.3044]},
    {"name": "Peshawar", "coordinates": [34.0769, 71.2489]},
    {"name": "Peshawar", "coordinates": [34.0099, 71.5693]},
    {"name": "Peshawar", "coordinates": [34.0278, 71.3038]},
    {"name": "Peshawar", "coordinates": [34.0148, 71.5679]},
    {"name": "Peshawar", "coordinates": [34.0156, 71.5814]},
    {"name": "Peshawar", "coordinates": [34.0212, 71.4828]},
    {"name": "Peshawar", "coordinates": [34.0053, 71.5571]},
    {"name": "Peshawar", "coordinates": [34.0107, 71.5622]},
    {"name": "Peshawar", "coordinates": [34.008, 71.5729]},
    {"name": "Peshawar", "coordinates": [34.0194, 71.581]},
    {"name": "Peshawar", "coordinates": [34.0224, 71.5776]},
    {"name": "Peshawar", "coordinates": [34.03, 71.545]},
    {"name": "Peshawar", "coordinates": [34.0122, 71.5715]},
    {"name": "Peshawar", "coordinates": [34.018, 71.569]},
    {"name": "Peshawar", "coordinates": [34.1047, 71.4172]},
    {"name": "Peshawar", "coordinates": [34.0039, 71.5524]},
    {"name": "Peshawar", "coordinates": [34.0132, 71.5731]},
    {"name": "Peshawar", "coordinates": [34.0009, 71.5693]},
    {"name": "Peshawar", "coordinates": [34.0138, 71.5837]},
    {"name": "Peshawar", "coordinates": [34.1474, 71.6546]},
    {"name": "Peshawar", "coordinates": [34.014, 71.576]},
    {"name": "Peshawar", "coordinates": [34.0206, 71.5653]},
    {"name": "Peshawar", "coordinates": [34.007, 71.5685]},
    {"name": "Peshawar", "coordinates": [34.0052, 71.5674]},
    {"name": "Peshawar", "coordinates": [33.95, 71.5]},
    {"name": "Peshawar", "coordinates": [34.006, 71.553]},
    {"name": "Peshawar", "coordinates": [34.0091, 71.5754]},
    {"name": "Peshawar", "coordinates": [34.0098, 71.5732]},
    {"name": "Peshawar", "coordinates": [34.0172, 71.5671]},
    {"name": "Peshawar", "coordinates": [34.024, 71.5486]},
    {"name": "Peshawar", "coordinates": [34.0128, 71.5699]},
    {"name": "Peshawar", "coordinates": [34.0093, 71.5735]},
    {"name": "Peshawar", "coordinates": [34.1157, 71.6215]},
    {"name": "Peshawar", "coordinates": [34.0135, 71.5833]},
    {"name": "Peshawar", "coordinates": [34.1699, 71.7131]},
    {"name": "Peshawar", "coordinates": [34.0163, 71.5717]},
    {"name": "Peshawar", "coordinates": [34.0225, 71.5333]},
    {"name": "Peshawar", "coordinates": [34.0168, 71.315]},
    {"name": "Peshawar", "coordinates": [34.1374, 72.0704]},
    {"name": "Peshawar", "coordinates": [34.1572, 71.3965]},
    {"name": "Peshawar", "coordinates": [34.0228, 71.571]},
    {"name": "Peshawar", "coordinates": [34.0131, 71.577]},
    {"name": "Peshawar", "coordinates": [34.0069, 71.5773]},
    {"name": "Peshawar", "coordinates": [34.0101, 71.5734]},
    {"name": "Peshawar", "coordinates": [34.0134, 71.5767]},
    {"name": "Peshawar", "coordinates": [34.1425, 71.611]},
    {"name": "Peshawar", "coordinates": [34.0078, 71.575]},
    {"name": "Peshawar", "coordinates": [34.0105, 71.5536]},
]

for location in tourist_locations:
    folium.Marker(
        location["coordinates"],
        popup=location["name"],
        icon=folium.Icon(color='blue')
    ).add_to(map)

# Display the map in the Streamlit app
folium_static(map)

# Conclusion and feedback collection
st.write("Thank you for using DiscoverPak - Your Travel Assistant!")
feedback = st.text_input("Please provide your feedback here:")
if st.button("Submit Feedback"):
    st.write("Thank you for your feedback!")
