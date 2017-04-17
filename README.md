# guitar-finder
Finds guitars, collects data about the listing, and reports notifications to the user

Dependencies:
* [Matplotlib](http://matplotlib.org/users/installing.html)
* [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* Tested with Python 3.5

Get started by running `python3 guitar_center_parser.py`...

### More info

This small script currently searches [Guitar Center's website](http://www.guitarcenter.com/Used/?Ntt=taylor%20314ce&Ns=r) for used Taylor 314ce guitars. It will build a list of available instruments, then email me about new guitars and changes in price. To search for a different guitar on their website, specify a different string for "search" in guitar_center_parser.py that is the URL of the search that you would get after looking directly on the site. Also, you will need to specify a keyword...more about that in a minute.

### Choosing a usable keyword

This tool is not designed to work with large results or a variety of types, but rather to help you find the best deal on a particular model. Your keyword should be in the title of *every* result that you wish to process. Fortunately, you don't really have to worry about this anymore...it is only used for the console output. It may be removed entirely at some point.

### Email

I now have the project configured to handle a gmail account correctly. The call to `Emailer()` at the beginning will prompt you for the password and everything immediately which will then be stored in a file. Note that the email is not protected in any way whatsoever. You can comment out this line when you are done entering the info. I built this to run as a `cron` process on my pi, so I wouldn't be able to type in the password each time as that is fully automated.

### Known issues

* Supports a max of 200 search results (only uses first page)

### License
* [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html)
* Copyright 2017 Jake Dube

[View on Github Pages](https://ekaj2.github.io/guitar-finder/)
