from flask import Flask
from flask import render_template
from flask import request
from flask import redirect


app = Flask(__name__)


@app.route('/story')
def create_page():
    """ Gets input through the user through the browser
    then adds them to the database
    """
    selected_story = []
    selected = ['', '', '', '', '']
    title = "Super Sprinter 3000 - Add new Story"
    id = ""
    desc_text = "Add new Story"
    return render_template('form.html', sel_list=selected_story, id=id,
                           selected=selected, title=title, desc_text=desc_text)


@app.route("/story", methods=['POST'])
def create_save():
    """ Gets several input from the user through the browser
    then writes them back to the datebase into a new line, with the next ID in line
    """
    title = request.form['title']
    story = request.form['story'].replace("\r\n", " ")
    criteria = request.form['criteria'].replace("\r\n", " ")
    business = request.form['business']
    estimation = request.form['estimation']
    progress = request.form['progress']
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split("ß¤") for item in data_list]
        next_id = ""
        if len(data_list) > 0:
            next_id = str(int(data_list[-1][0]) + 1)
        else:
            next_id = 0
    with open('database.csv', 'a') as file:
        file.write(str(next_id) + "ß¤")
        file.write(str(title + "ß¤"))
        file.write(str(story + "ß¤"))
        file.write(str(criteria + "ß¤"))
        file.write(str(business + "ß¤"))
        file.write(str(estimation + "ß¤"))
        file.write(str(progress + "\n"))
    return redirect("/list")


@app.route("/story/<int:id>", methods=["GET"])
def update_show(id):
    """Receives an ID from the user through the browser, then find the
    correct the story and returns all the values from the database to the html form
    """
    title = "Super Sprinter 3000 - Edit Story"
    desc_text = "Edit Story"
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split("ß¤") for item in data_list]
        selected_story = []
        for item in data_list:
            if int(item[0]) == int(id):
                selected_story = item

        options = ["1. Planning", "2. TODO", "3. In Progress", "4. Review", "5. Done"]
        selected_status = ['', '', '', '', '']
        for i in range(len(selected_status)):
            if selected_story[6] == options[i]:
                selected_status[i] = "selected"
        return render_template('form.html', sel_list=selected_story, id=('/' + str(id)),
                               selected=selected_status, title=title, desc_text=desc_text)


@app.route("/story/<int:id>", methods=['POST'])
def update_save(id):
    """ Receives several inputs from the user through the browser then
    finds the correct row with the ID then changes the values and writes it back, updates it
    then returns the user back to the list page
    """
    title = request.form['title']
    story = request.form['story'].replace("\r\n", " ")
    criteria = request.form['criteria'].replace("\r\n", " ")
    business = request.form['business']
    estimation = request.form['estimation']
    progress = request.form['progress']
    new_list = [str(id), title, story, criteria, business, estimation, progress]
    selected_row = []
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split("ß¤") for item in data_list]
        for item in data_list:
            if int(item[0]) == int(id):
                selected_row.append(new_list)
            else:
                selected_row.append(item)

    with open('database.csv', 'w') as file:
        for item in selected_row:
            file.write("ß¤".join(item) + "\n")
    return redirect("/list")


@app.route("/", methods=['GET'])
@app.route("/list", methods=['GET'])
def main_list():
    """ Reads the database into list of lists then returns them to the html template
    """
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split("ß¤") for item in data_list]
    title = "Super Sprinter 3000"
    return render_template('list.html', data_list=data_list, title=title)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    """Receives an ID from the user through the browser, then searches the database
    for said ID, if it finds it then it deletes it, then returns the user back to the
    list page
    """
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split("ß¤") for item in data_list]
        for item in data_list:
            if int(item[0]) == int(id):
                data_list.remove(item)

    with open('database.csv', 'w') as file:
        for item in data_list:
            datas = "ß¤".join(item)
            file.write(str(datas) + "\n")
    return render_template('list.html', data_list=data_list, id=('/' + str(id)))


@app.route("/search", methods=['POST'])
def search():
    """ Receives a string from the user through forms then
    searches the database if the string is in any row item,
    it it is then returns the whole row, if not then goes back to the main page
    """
    title = "Super Sprinter 3000"
    searched_word = request.form['search']
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split("ß¤") for item in data_list]
        searched_row = []
        for row in data_list:
            for item in row:
                if str(searched_word) in item:
                    searched_row.append(row)
        if len(searched_word) > 0:
            return render_template('list.html', data_list=searched_row, title=title)
        else:
            return redirect("/list")


@app.route("/sortby", methods=['POST'])
def sortby():
    """ gets input from the user through the browser, then
    shows the database based on that rule
    """
    title = "Super Sprinter 3000"
    search_key = str(request.form['sortby'])
    with open('database.csv') as data:
        data_list = data.read().splitlines()
        data_list = [item.split("ß¤") for item in data_list]
        if search_key == 'ID':
            data_list = sorted(data_list, key=lambda x: int(x[0]))
        elif search_key == 'Title':
            data_list = sorted(data_list, key=lambda x: str(x[1]))
        elif search_key == 'User Story':
            data_list = sorted(data_list, key=lambda x: str(x[2]))
        elif search_key == 'Acceptance Criteria':
            data_list = sorted(data_list, key=lambda x: str(x[3]))
        elif search_key == 'Business Value':
            data_list = sorted(data_list, key=lambda x: int(x[4]))
        elif search_key == 'Estimation (h)':
            data_list = sorted(data_list, key=lambda x: float(x[5]))
        elif search_key == 'Status':
            data_list = sorted(data_list, key=lambda x: str(x[6]))
    return render_template('list.html', data_list=data_list, title=title)


if __name__ == "__main__":
    app.run(debug=None)
