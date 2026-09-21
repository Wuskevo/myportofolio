Name : Clement Kevin Tanadi

NPM : 2506632892

Class : PBP B

### Assignment 1

#### 1. HTML5 sematic elements
Designing the HTML structure, I used both `<section>` and `<article>` but not `<aside>`. I used them instead of `<div>`s to enforce that they are not merely aesthetics or layout and that their children share a common theme. I specifically made each project card an article because each one of them should still have the same meaning (that is a project card) when moved somewhere else. I haven't yet used the `<aside>` as I have not yet gotten an idea on what to use it for.
#### 2. Responsive CSS layout challenges
Most of the CSS was made using the tutorial's template for reference with only some tweaks to color and radius for personal preference so I did not experience any responsive issues on different screen sizes so far. Most of the numbers in the stylesheet currently are just the result of trial and error. I used a placeholder CSS rule template from Claude (001/1) where consistency and common UI conventions were prioritized. I asked for a cheatsheet on CSS so I may make my own modifications. Overall, the current style is decent enough for now, and I will refine it later.
#### 3. Limitations of a static web
The most noticeable limitation I experienced using a static web thus far was having to manually add content in HTML which is definitely not efficient. One thing I would really like to implement in next iterations is a dashboard or content management system so I don't need to type and add stuff repeatedly into HTML.

### Assignment 2

#### 1. MVT Flow
When a user opens the new portfolio page, their request gets passed to Django and Django then matches that URL to a view through the project's urls.py, the view then retrieves and processes model data to be forwarded as rendering context for a template, the presentation structure layer. The Model here defines and manages data with the help of a database. Finally, Django returns the rendered template (HTML) + context as a response that appears in the browser. There are two urls.py for the purpose of keeping things organized and not having one giant urls file that contains the paths for every app. An app, a self-contained section that does one specific job, should own and handle its own URL patterns. Therefore, all that the project's urls.py needs to do is to delegate url paths; delegation to main app, for instance, can be done using the include function from django.urls and passing in main.urls with the "" prefix, making all requests with the "" prefix be forwarded to main's urls.py instead. Main's urls.py then matches the remaining path to a specific view, finishing the broad-routing from project and specific-routing from app.

#### 2. Storing Data in a Model instead of a Template
A rule that I've heard in GameDev that applies here is the separation of visuals and data. Templates (.html) are supposed to only be resposible for presentation, so the data should not be hardcoded there and instead models so that data can be properly stored in a database. As a result, maintenance is far far far easier and more practical as you need only change the data in the database instead of changing it in a markdown language that is html.


#### 3. `makemigrations` vs `migrate`
The comamnds makemigrations and migrate in Django are analogous to git's add and commit. More precisely, the former is for planning while the latter actually executes or commits to said plan. Makemigrations creates the migration files that describe the differences between the current model's definitions (in models.py) against the last known state it has recorded without touching the database yet. On the contrary, migrate reads the migration files (including ones that you haven't applied yet) and executes the corresponding SQL against the database, altering tables. 

### Assignment 3

#### 1. ModelForm and CSRF Token Mechanics

Imagine you are ordering custom furniture. Building an HTML form manually is like drawing the furniture diagram by hand, writing down all the measurement checks on a separate sheet, and manually typing the specs into the factory machine. In Django, this means re-writing `<input>` tags, writing code in `views.py` to manually pull every single field out of `request.POST`, writing checks to verify if numbers or dates are valid, and manually calling `.save()`. Django’s `ModelForm` acts like a smart automated template: it inspects your database blueprint (`models.py`), auto-generates the HTML form fields, checks submitted data automatically via `form.is_valid()`, and saves it directly to the database using `form.save()`.

Imagine you are logged into your online banking page, and you accidentally visit a shady website in another tab. That shady site secretly tries to trick your browser into sending a "transfer money" command to your bank; because your browser automatically includes your saved login credentials, the bank might mistakenly think *you* clicked it. To block this trick, the `{% csrf_token %}` tag places a hidden secret code inside your official form. When you submit it, Django's background security check verifies that the hidden code matches your active browser session. Because browsers strictly forbid sneaky websites from peeking at data belonging to other websites, the shady site cannot steal or guess that code, and the fake command gets thrown away instantly.

#### 2. JSON vs. XML in Modern Web Applications

JSON is like a clean, minimal shopping list, while XML is like filling out a heavy, double-enveloped government form. Web browsers speak JavaScript natively, and JSON uses the exact same layout as JavaScript objects, meaning a browser can turn JSON into usable data almost instantly using high-speed, built-in engine tools like `JSON.parse()`. In contrast, XML has no built-in concept of a simple list and forces you to wrap list items in verbose, repetitive tags like `<items><item>...</item></items>`, requiring the browser to build a structural tree heavy on memory just to extract the data. Stripping away XML's endless closing tags also makes JSON files much smaller, saving valuable network bandwidth over mobile and web connections.

Even though JSON is great for most everyday tasks, XML is still the go-to when you need really strict rules or are working with complex documents. Think of XML like a rigid, official building blueprint: it has strict rulebooks that force massive companies to follow the exact same data layout, and it has built-in labels to prevent confusion if two different systems use the exact same name. Most importantly, XML lets you mix regular sentences and formatting tags together seamlessly. For instance, writing a paragraph where a word can be bolded right in the middle (`<p>Hello <b>world</b></p>`). JSON struggles with this kind of document editing because it keeps text and data structure separate, forcing you to stuff messy formatting codes inside regular text strings instead.

#### 3. View-to-JSON Flow and the Serialization Process

When a user requests your portfolio, the URL dispatcher directs the request to a view function. The view queries the database, which returns a `QuerySet`, which is a list of living Python model objects. Because a `QuerySet` is a complex Python object packed with database connections, methods, and special types (like `datetime` or foreign key links), standard web text tools like `json.dumps()` don't know how to handle it and will crash with a `TypeError`. The view passes the `QuerySet` through a "serializer", which strips away the Python-specific code and translates the model fields into simple universal primitives (strings, numbers, dictionaries). Think of serialization like dismantling a fully assembled bicycle (the complex Python object) into a flat cardboard box of raw parts (JSON text) so it can fit through a narrow postal pipe across the internet in a `JsonResponse`.

Once that JSON arrives at a client (like a mobile app or frontend JavaScript), the client unpacks the data and displays it. However, if your Django server is already building the final HTML page itself on the backend, converting your database models into JSON text and then immediately converting them back into Python objects creates completely unnecessary extra work. For traditional server-rendered HTML pages, you should skip serialization entirely and pass the raw database `QuerySet` directly into Django's `render()` function.

## AI Disclosure

### How I used CoPilot in expediting assignment 3
- I used CoPilot to refactor tests.py into smaller scripts so that I can focus on one entity per script instead of having one God Class.
- I used CoPilot to quickly rename the files to match the convention used in the tutorial (pluralized)
- I only dared to use CoPilot or AI to generate stuff I can do myself but to save time since I am also juggling with a competition, I needed a lot of help, only reviewing the code and adding some minor adjustments. My CoPilot wasn't that great at initiatively making good code practices, so I had to make some refactors as shown from the commit before this.

### Chat History 

The following will use the format:

`[id]` / `[assignment/tutorial index]` - `[short description]`: `[link to chat]`

#### 001 / 1 - CSS placeholder for the 3 sections (projects, experiences, skills): https://claude.ai/share/b9812bca-8eaa-4510-8d65-12f35458be03

#### 002 / 2 - Icons from ionicons: https://claude.ai/share/c31ecc8a-9044-4c30-91e3-59218f337dec
Help to display icons to add more visuals to the portofolio

#### 003 / 2 - Credential grouping by category: https://claude.ai/share/b4c95896-1bee-4278-8187-eb3987f4bdef
Guidance in building the credential model and presentation with the use of python dictionary comprehension to group by categories (as a dict in the context)

#### 004 / 2 - Style tokenization: https://claude.ai/share/45a651fa-1349-4588-b477-3a1dc7ae045c
Drastically improved the quality of style.css by tokenizing magic values and documenting them

## TODOS & Suggestions

- ~~Keep experience and credential tests in separate files under `main/tests/`.~~
- ~~Add a test whenever a CRUD action, JSON endpoint, or form field changes.~~
- Consider sharing a queryset helper instead of calling JSON views from display views.
- Extract repeated credential category markup into a reusable template component.
- Add browser coverage for opening, cancelling, and confirming delete modals.
- Run `python manage.py check` and `python manage.py test` before submitting changes.


