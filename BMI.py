'''Create a program for a BMI calculator that takes the name, age, height, and weight of a person and stores the data into a file.
 Allow the application to show weather the user is Underweight, Overweight, Obese, or Normal.
 Make sure you add validation rules.
 Add a ‘Show Graph’ button that display a pie chart of the data stored, showing the percentage of people under certain BMI categories.
 Challenge: Can you allow the chart to show on the same window? You may need to use another library'''
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_bmi():
    try:
        weight = float(weightentry.get())
        height = float(heightentry.get())

        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid Input", "Height and weight must be positive values.")
            return None, None

        height_in_meters = height / 100
        bmi = weight / (height_in_meters ** 2)

        if bmi < 18.5:
            category = "Underweight"
            messagebox.showinfo("BMI Category", "Underweight")
        elif bmi < 25:
            category = "Normal"
            messagebox.showinfo("BMI Category", "Normal")
        elif bmi < 30:
            category = "Overweight"
            messagebox.showinfo("BMI Category", "Overweight")
        else:
            category = "Obese"
            messagebox.showinfo("BMI Category", "Obese")

        return round(bmi, 2), category
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for weight and height.")
        return None, None


def save_data():
    fname = fnameentry.get()
    weight = weightentry.get()
    height = heightentry.get()

    bmi, category = calculate_bmi()

    if fname != '' and height != '' and weight != '' and bmi is not None:
        age = agespinbox.get()

        with open('bmidata.txt', 'a') as filewrite:
            filewrite.write(
                str(fname) + ',' + str(age) + ',' + str(weight) + ',' + str(height) + ','
                + str(bmi) + ',' + str(category)+'\n')

        messagebox.showinfo("Data Saved", "Data has been successfully saved.")
    else:
        messagebox.showwarning(title='Error: Missing Data', message='First Name, Height and Weight are Required to save data!')


def show_pie_chart():
    underweight = 0
    normal = 0
    overweight = 0
    obese = 0

    try:
        with open('bmidata.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                # Ensure there are enough parts to access the category
                if len(parts) > 5:
                    category = parts[5]
                    if category == "Underweight":
                        underweight += 1
                    elif category == "Normal":
                        normal += 1
                    elif category == "Overweight":
                        overweight += 1
                    elif category == "Obese":
                        obese += 1
    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the file: {e}")
        return

    if underweight == 0 and normal == 0 and overweight == 0 and obese == 0:
        messagebox.showwarning("No Data", "No BMI data available to display.")
        return

    categories = ["Underweight", "Normal", "Overweight", "Obese"]
    sizes = [underweight, normal, overweight, obese]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(sizes, labels=categories, autopct='%1.0f%%', startangle=90)
    ax.set_title("BMI Categories Distribution")
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=pie_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


window = tk.Tk()
window.title('BMI Calculation')

frame = tk.Frame(window)
frame.pack()

userinfoframe = tk.LabelFrame(frame, text='User Information')
userinfoframe.grid(row=0, column=0)

fnamelabel = tk.Label(userinfoframe, text='First Name')
fnamelabel.grid(row=0, column=0)

fnameentry = tk.Entry(userinfoframe)
fnameentry.grid(row=0, column=1)

agelabel = tk.Label(userinfoframe, text='Age')
agelabel.grid(row=0, column=2)

agespinbox = tk.Spinbox(userinfoframe, from_=18, to=100)
agespinbox.grid(row=0, column=3)

weightlabel = tk.Label(userinfoframe, text='Weight (kg)')
weightlabel.grid(row=1, column=0)

weightentry = tk.Entry(userinfoframe)
weightentry.grid(row=1, column=1)

heightlabel = tk.Label(userinfoframe, text='Height (cm)')
heightlabel.grid(row=1, column=2)

heightentry = tk.Entry(userinfoframe)
heightentry.grid(row=1, column=3)

calcbtn = tk.Button(userinfoframe, text="Calculate", command=calculate_bmi)
calcbtn.grid(row=2, column=1)

savebtn = tk.Button(userinfoframe, text='Save', command=save_data)
savebtn.grid(row=2, column=2)

piebtn = tk.Button(userinfoframe, text="Show Pie Chart", command=show_pie_chart)
piebtn.grid(row=3, column=1, columnspan=2, pady=10)

pie_frame = tk.Frame(window)
pie_frame.pack(pady=10)

window.mainloop()
