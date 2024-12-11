from flask import Flask, request, jsonify, render_template
import random
import pandas as pd

app = Flask(__name__)

# List of names
names = ["Abhirami", "Sheethu", "Priya", "Navaneeth", "Girish", "Malavika", 
         "Balan", "Indu", "Shobhana", "Sandeep", "Nandana", "Madhav", "Maheshwar"]

# Shuffle the names and create a friend list
random.shuffle(names)
friendlist = {names[i]: names[(i + 1) % len(names)] for i in range(len(names))}

# Save the friend list to an Excel file
df = pd.DataFrame(list(friendlist.items()), columns=["Name", "Christmas Friend"])
df.to_excel("Friends_List.xlsx", index=False)

# Set to keep track of names that have already checked their friends
queried_names = set()

# Routes
@app.route("/")
def home():
    return render_template("christmas.html")  # Serve the HTML file

@app.route("/get_friend", methods=["POST"])
def get_friend():
    name = request.form.get("name").strip()
    
    if name not in names:
        return jsonify({"error": "Name not found. Please check your spelling and try again."})
    
    if name in queried_names:
        return jsonify({"error": "You can only check your Christmas friend once!"})
    
    queried_names.add(name)
    return jsonify({"friend": friendlist[name]})

if __name__ == "__main__":
    app.run(debug=True)
