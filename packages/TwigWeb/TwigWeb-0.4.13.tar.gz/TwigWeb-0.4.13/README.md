# Twig 0.4.13

Twig is a backend web framework for python utilizing the **socket** module to handle http requests and serve responses.

To install use the following command:
```cli
py -m pip install TwigWeb
```

### Changelog

---

**0.4.0**

 - Added dynamic route parameters.

 - Improved route handling with Route class

---

**0.3.0**

 - Added static paths and folders functions.

 - Added element class.

 - Added component classes.

---

**0.2.0**

 - Added `set_all_routes` function

 - Fixed inconsistent request handling

 - Improved documentation

---

### REST API example

This example shows how to make a basic REST API with Twig that adds 2 numbers together, and an example use case for the component system.  It includes all the current functionalities of Twig.

Example *main.py*:

```py
import random
import time
from typing import Dict
from TwigWeb.backend import Server, ContentType, Response as res
from componenttest import Card, Dashboard

# SERVER CONSTRUCTOR EXAMPLE

app = Server("", verbose=False, open_root=False, debug=True)

# ---PARAMETERS--- #
#
# verbose will show the full request each time when True.
#
# open_root will open the index of the site in a web browser every time the server runs when True.
#
# debug will show any request errors when True.
#
# ---------------- #

# ADD STATIC FILE EXAMPLE

app.add_static("test.jpg")

# SET STATIC FILES (this overwrites any static files you've added before)

app.set_static({"test.jpg"})

# ADD STATIC FOLDER EXAMPLE

app.add_static_folder("test")

# SET STATIC FOLDERS (this overwrites any static folders you've added before)

app.set_static_folders({"test"})

# ---ABOUT--- #
#
# Static files are files that can be accessed by clients without declaring a route
#function.  Any file that is within a static folder is also treated as a static file.
#
# ----------- #


# COMPONENT EXAMPLE (See component.py example)
def card(headers: Dict[str, str]):
    return res.Response(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
{Dashboard(cardlist = [
    {
        "name": "William",
        "date": time.strftime("%H:%M:%S", time.localtime()),
        "title": "Component test",
        "content": f"""This is a test of the component system.{
            Card(
                name = "Also William",
                date = time.strftime("%H:%M:%S", time.localtime()),
                title = "Nested Component",
                content = "This is a test of nested components."
            )
        }"""
    },
    {
        "name": "Jeff",
        "date": time.strftime("%H:%M:%S", time.localtime()),
        "title": "Jeff's First Post",
        "content": "Hi my name is Jeff and this is my first post!"
    }
])}
</body>
</html>
''', ContentType.html)


# SET ALL ROUTES EXAMPLE

app.set_all_routes({
    "card": card
})

# ---ABOUT--- #
# this overwrites all routes in the app with new routes. This is so you can
#have all your routes in a separate file from their functions if you wanted.
# ----------- #


# ROUTE DECORATOR EXAMPLES

# ---ABOUT--- #
# Creates a path in the server for that function.  The path is whatever is
#supplied to the decorator as an argument
#
# Important!!!: every route function must include an argument for headers
#even if route function does not use any headers. 
# ----------- #

# json example
@app.route("apiexample/json")
def test_json(headers: Dict[str, str]):
    return res.Response(f"[{random.randint(0,100)},{random.randint(0,100)},{random.randint(0,100)}]", ContentType.json)

# plaintext example
@app.route("apiexample/plain")
def test_plain(headers: Dict[str, str]):
    return res.Response("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", ContentType.plain)

# css example
@app.route("apiexample/css")
def test_css(headers: Dict[str, str]):
    return res.Response(res.read("index.css"), ContentType.css)

# wasm example
@app.route("apiexample/wasm")
def test_css(headers: Dict[str, str]):
    return res.Response(res.read("example.wasm"), ContentType.wasm)

# headers example
@app.route("apiexample")
def test_headers(headers: Dict[str, str]):
    sum = int(headers["num-1"]) + int(headers["num-2"])
    return res.Response(f'{{"result":{sum}}}', ContentType.json)

# html example
@app.route("")
def index(headers: Dict[str, str]):
    return res.Response(res.read("index.html"))

# dynamic route example
@app.route("dynamic/(string_var_name)/[int_var_name]")
def dynamic_example(headers: Dict[str, str], route_parameters:Dict[str, str | int]):
    return res.Response(f"""string:{route_parameters["string_var_name"]} int:{route_parameters["int_var_name"]}""")

# MANUALLY SET ROUTE EXAMPLE

def manual_route(headers: Dict[str, str]):
    return res.Response('{"message":"Hello"}', ContentType.json)

app.set_route("manual", manual_route)

# ---ABOUT--- #
# this does the same thing as the @app.route() decorator and can be
#used to set routes for functions in external files.
# ----------- #

# Running the server
app.run()
```

Example *index.html*:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
    <input type="number" id="num1" value="0">
    +
    <input type="number" id="num2" value="0">
    =
    <span id="Content">
        
    </span>
    <div><button id="solve">solve</button></div>
    <script>
        const CONTENT_DIV = document.getElementById("Content")
        document.getElementById("solve").addEventListener("click", async_solve)
        async function async_solve(){
            let num1 = parseInt(document.getElementById("num1").value)
            let num2 = parseInt(document.getElementById("num2").value)
            const res = await fetch("/apiexample", {method:'POST', headers:{
                "num-1":num1,
                "num-2":num2
            }})
            const res_json = await res.json()
            CONTENT_DIV.innerText = res_json.result
        }
        async_solve()
    </script>
</body>
</html>
```

Example *component.py*:

```py
from TwigWeb.frontend import Component, Element as E


class Card(Component):
    """Components are classes that inherit from the Component class."""
    def hydrate(self):
        name = self.props["name"]
        date = self.props["date"]
        title = self.props["title"]
        content = self.props["content"]
        
        return E("div", {
            "style": "background-color: gray; margin: 5px; border: solid; border-radius: 10px;",
            "id":f"{name}"
        }, [
            E("div", {"style": "display: flex; justify-content: space-between;"}, [
                E("div", {"style": "font-size: 20px; padding: 5px;"}, [f"{name}"]),
                E("div", {"style": "font-size: 15px; padding: 5px;"}, [f"{date}"]),
            ]),
            E("h3", {"style": "text-align: center;"}, [f"{title}"]),
            E("div", {"style": "padding: 10px; font-style: italic;"}, [f"{content}"]),
        ]).render()

class Dashboard(Component):
    """The Dashboard component takes in a list of dictionaries with all of the cards data
    and constructs cards with that data inside of the Dashboard component.  Comprehension
    can be used to create a workflow similar to React.js."""
    def hydrate(self):
        return E("div", {"style": "background-color: black; color: white; padding: 10px;"}, [
            E("h1", {}, ["DASHBOARD"]),
            E("div", {}, [f"""{Card(
                name = card["name"],
                date = card["date"],
                title = card["title"],
                content = card["content"]
            )}""" for ind, card in enumerate(self.props["cardlist"])])
        ]).render()
```
