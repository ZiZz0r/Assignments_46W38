import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot()

# Set labels and title
pie_labels = ["Crude Oil", "Natural Gas", "Renewable energy", "Solid fuels", "Nuclear energy"]
pie_sizes = [37.7, 20.4, 19.5, 10.6, 11.8]
pie_colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"]

ax.pie(pie_sizes, labels=pie_labels, colors=pie_colors, autopct='%1.1f%%')
ax.set_title("EU Energy Sources Distribution (2023)", fontsize=16)
plt.show()
