import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("zomato.csv", encoding='latin-1')

# Drop rows with missing critical data
df = df.dropna(subset=['City', 'Cuisines', 'Rating text', 'Average Cost for two'])

# Map city to restaurants
city_restaurant_map = {}
for city in df['City'].unique():
    restaurants = df[df['City'] == city]['Restaurant Name'].unique()
    city_restaurant_map[city] = list(restaurants)

# Drop irrelevant columns except Restaurant Name
df.drop(columns=[
    'Restaurant ID', 'Address', 'Locality',
    'Longitude', 'Latitude', 'Currency', 'Rating color'
], inplace=True)

# Encode categorical variables
le_city = LabelEncoder()
df['City_enc'] = le_city.fit_transform(df['City'])

le_cuisine = LabelEncoder()
df['Cuisines_enc'] = le_cuisine.fit_transform(df['Cuisines'])

# Binary encoding for these columns
for col in ['Has Table booking', 'Has Online delivery', 'Is delivering now']:
    df[col] = LabelEncoder().fit_transform(df[col])

# Target variable encoding
le_rating = LabelEncoder()
df['Target'] = le_rating.fit_transform(df['Rating text'])

# Features for model
feature_cols = [
    'City_enc', 'Cuisines_enc', 'Has Table booking',
    'Has Online delivery', 'Is delivering now',
    'Average Cost for two', 'Price range',
    'Aggregate rating', 'Votes'
]

X = df[feature_cols]
y = df['Target']

# Scale features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = LogisticRegression(multi_class='multinomial', max_iter=500)
model.fit(X_scaled, y)

# Store features by restaurant for GUI
restaurant_features = df.set_index('Restaurant Name')[feature_cols]

def get_model_data():
    return model, scaler, le_city, le_cuisine, le_rating, city_restaurant_map, restaurant_features, feature_cols
