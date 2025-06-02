import tkinter as tk
from tkinter import messagebox
from model import get_model_data

# Load model and encoders
model, scaler, le_city, le_cuisine, le_rating, city_restaurant_map, restaurant_features, feature_cols = get_model_data()

root = tk.Tk()
root.title("Restaurant Rating Predictor")
root.geometry("600x600")
root.configure(bg="#f9f9f9")

tk.Label(root, text="Restaurant Rating Prediction", font=("Helvetica", 16, "bold"), bg="#f9f9f9").pack(pady=10)

# City dropdown
tk.Label(root, text="Select City:", bg="#f9f9f9").pack()
city_var = tk.StringVar(value=list(city_restaurant_map.keys())[0])
city_menu = tk.OptionMenu(root, city_var, *city_restaurant_map.keys())
city_menu.pack()

# Restaurant dropdown
tk.Label(root, text="Select Restaurant:", bg="#f9f9f9").pack()
restaurant_var = tk.StringVar()
restaurant_menu = tk.OptionMenu(root, restaurant_var, "")
restaurant_menu.pack()

# Frame for inputs
inputs_frame = tk.Frame(root, bg="#f9f9f9")
inputs_frame.pack(pady=10)

# Cuisine (readonly)
cuisine_var = tk.StringVar()
tk.Label(inputs_frame, text="Cuisine:", bg="#f9f9f9").grid(row=0, column=0, sticky='w', padx=5, pady=5)
cuisine_entry = tk.Entry(inputs_frame, textvariable=cuisine_var, state='readonly')
cuisine_entry.grid(row=0, column=1, pady=5, sticky='w')

# Input fields dict
input_fields = {}

def make_option_menu(row, label_text, var, options=('0', '1')):
    tk.Label(inputs_frame, text=label_text, bg="#f9f9f9").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    option_menu = tk.OptionMenu(inputs_frame, var, *options)
    option_menu.grid(row=row, column=1, sticky='w')

def make_entry(row, label_text, default):
    tk.Label(inputs_frame, text=label_text, bg="#f9f9f9").grid(row=row, column=0, sticky='w', padx=5, pady=5)
    entry = tk.Entry(inputs_frame)
    entry.grid(row=row, column=1, sticky='w')
    entry.insert(0, default)
    return entry

# Flags (0/1)
input_fields['Has Table booking'] = tk.StringVar(value='1')
make_option_menu(1, "Has Table booking (0=No,1=Yes):", input_fields['Has Table booking'])

input_fields['Has Online delivery'] = tk.StringVar(value='1')
make_option_menu(2, "Has Online delivery (0=No,1=Yes):", input_fields['Has Online delivery'])

input_fields['Is delivering now'] = tk.StringVar(value='0')
make_option_menu(3, "Is delivering now (0=No,1=Yes):", input_fields['Is delivering now'])

# Numeric entries
input_fields['Average Cost for two'] = make_entry(4, "Average Cost for two:", "1000")
input_fields['Price range'] = make_entry(5, "Price range (1-4):", "2")
input_fields['Aggregate rating'] = make_entry(6, "Aggregate rating (0.0-5.0):", "4.0")
input_fields['Votes'] = make_entry(7, "Votes:", "100")

# Update restaurant menu when city changes
def update_restaurant_menu(*args):
    city = city_var.get()
    restaurants = city_restaurant_map.get(city, [])
    menu = restaurant_menu['menu']
    menu.delete(0, 'end')
    if restaurants:
        restaurant_var.set(restaurants[0])
        for r in restaurants:
            menu.add_command(label=r, command=lambda val=r: restaurant_var.set(val))
        update_features_from_restaurant(restaurants[0])
    else:
        restaurant_var.set("")
        clear_inputs()

city_var.trace_add('write', update_restaurant_menu)

def clear_inputs():
    cuisine_var.set("")
    input_fields['Has Table booking'].set('0')
    input_fields['Has Online delivery'].set('0')
    input_fields['Is delivering now'].set('0')
    for key in ['Average Cost for two', 'Price range', 'Aggregate rating', 'Votes']:
        input_fields[key].delete(0, tk.END)
        input_fields[key].insert(0, "")

def update_features_from_restaurant(restaurant_name):
    try:
        row = restaurant_features.loc[restaurant_name]
        cuisine_code = int(row['Cuisines_enc'])
        cuisine_name = le_cuisine.inverse_transform([cuisine_code])[0]
        cuisine_var.set(cuisine_name)

        input_fields['Has Table booking'].set(str(row['Has Table booking']))
        input_fields['Has Online delivery'].set(str(row['Has Online delivery']))
        input_fields['Is delivering now'].set(str(row['Is delivering now']))

        input_fields['Average Cost for two'].delete(0, tk.END)
        input_fields['Average Cost for two'].insert(0, str(row['Average Cost for two']))

        input_fields['Price range'].delete(0, tk.END)
        input_fields['Price range'].insert(0, str(row['Price range']))

        input_fields['Aggregate rating'].delete(0, tk.END)
        input_fields['Aggregate rating'].insert(0, str(row['Aggregate rating']))

        input_fields['Votes'].delete(0, tk.END)
        input_fields['Votes'].insert(0, str(row['Votes']))

    except Exception:
        clear_inputs()

restaurant_var.trace_add('write', lambda *args: update_features_from_restaurant(restaurant_var.get()))

# Initialize restaurant menu on load
update_restaurant_menu()

def predict():
    try:
        city_name = city_var.get()
        cuisine_name = cuisine_var.get()
        city_code = le_city.transform([city_name])[0]
        cuisine_code = le_cuisine.transform([cuisine_name])[0]

        input_values = [
            city_code,
            cuisine_code,
            int(input_fields['Has Table booking'].get()),
            int(input_fields['Has Online delivery'].get()),
            int(input_fields['Is delivering now'].get()),
            float(input_fields['Average Cost for two'].get()),
            int(input_fields['Price range'].get()),
            float(input_fields['Aggregate rating'].get()),
            int(input_fields['Votes'].get())
        ]

        scaled_input = scaler.transform([input_values])
        pred_code = model.predict(scaled_input)[0]
        pred_label = le_rating.inverse_transform([pred_code])[0]

        messagebox.showinfo("Prediction Result", f"Predicted Rating: {pred_label}")

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input or error:\n{e}")

tk.Button(root, text="Predict Rating", command=predict, bg="#4caf50", fg="white", font=("Arial", 12), width=20).pack(pady=20)

root.mainloop()
