Name : Clement Kevin Tanadi

NPM : 2506632892

Class : PBP B

### Assignment 1

1. Designing the HTML structure, I used both `<section>` and `<article>` but not `<aside>`. I used them instead of `<div>`s to enforce that they are not merely aesthetics or layout and that their children share a common theme. I specifically made each project card an article because each one of them should still have the same meaning (that is a project card) when moved somewhere else. I haven't yet used the `<aside>` as I have not yet gotten an idea on what to use it for.
2. Most of the CSS was made using the tutorial's template for reference with only some tweaks to color and radius for personal preference so I did not experience any responsive issues on different screen sizes so far. Most of the numbers in the stylesheet currently are just the result of trial and error. I used a placeholder CSS rule template from Claude (001/1) where consistency and common UI conventions were prioritized. I asked for a cheatsheet on CSS so I may make my own modifications. Overall, the current style is decent enough for now, and I will refine it later.
3. The most noticeable limitation I experienced using a static web thus far was having to manually add content in HTML which is definitely not efficient. One thing I would really like to implement in next iterations is a dashboard or content management system so I don't need to type and add stuff repeatedly into HTML.

### Assignment 2

1. When a user opens the new portfolio page, their request gets passed to Django and Django then matches that URL to a view through the project's urls.py, the view then retrieves and processes model data to be forwarded as rendering context for a template, the presentation structure layer. The Model here defines and manages data with the help of a database. Finally, Django returns the rendered template (HTML) + context as a response that appears in the browser. There are two urls.py for the purpose of keeping things organized and not having one giant urls file that contains the paths for every app. An app, a self-contained section that does one specific job, should own and handle its own URL patterns. Therefore, all that the project's urls.py needs to do is to delegate url paths; delegation to main app, for instance, can be done using the include function from django.urls and passing in main.urls with the "" prefix, making all requests with the "" prefix be forwarded to main's urls.py instead. Main's urls.py then matches the remaining path to a specific view, finishing the broad-routing from project and specific-routing from app.
2. A rule that I've heard in GameDev that applies here is the separation of visuals and data. Templates (.html) are supposed to only be resposible for presentation, so the data should not be hardcoded there and instead models so that data can be properly stored in a database. As a result, maintenance is far far far easier and more practical as you need only change the data in the database instead of changing it in a markdown language that is html.
3. The comamnds makemigrations and migrate in Django are analogous to git's add and commit. More precisely, the former is for planning while the latter actually executes or commits to said plan. Makemigrations creates the migration files that describe the differences between the current model's definitions (in models.py) against the last known state it has recorded without touching the database yet. On the contrary, migrate reads the migration files (including ones that you haven't applied yet) and executes the corresponding SQL against the database, altering tables. 

## AI Disclosure

The following will use the format:

`[id]` / `[assignment/tutorial index]` - `[short description]`: `[link to chat]`

#### 001 / 1 - CSS placeholder for the 3 sections (projects, experiences, skills): https://claude.ai/share/b9812bca-8eaa-4510-8d65-12f35458be03

#### 002 / 2 - Icons from ionicons: https://claude.ai/share/c31ecc8a-9044-4c30-91e3-59218f337dec
Help to display icons to add more visuals to the portofolio

#### 003 / 2 - Credential grouping by category: https://claude.ai/share/b4c95896-1bee-4278-8187-eb3987f4bdef
Guidance in building the credential model and presentation with the use of python dictionary comprehension to group by categories (as a dict in the context)

#### 004 / 2 - Style tokenization: https://claude.ai/share/45a651fa-1349-4588-b477-3a1dc7ae045c
Drastically improved the quality of style.css by tokenizing magic values and documenting them

