## lineNdots
A bare-bones template for Python packages, ready for use with setuptools (PyPI), pip, and py.test.

### Using this as a template
Let's assume that you want to create a small scientific Python project called `smallish`.

To use this repository as a template, click the green "use this template" button on the front page of the "lineNdots" repository.

In "Repository name" enter the name of your project. For example, enter `smallish` here. After that, you can hit the "Create repository from template" button.

You should then be able to clone the new repo into your machine. You will want to change the names of the files. For example, you will want to move `lineNdots/lineNdots.py` to be called `smallish/smallish.py`
```
git mv lineNdots smallish
git mv smallish/lineNdots.py smallish/smallish.py
git mv smallish/tests/test_lineNdots.py smallish/tests/test_smallish.py
```

Make a commit recording these changes. Something like:
```
git commit -a -m "Moved names from `lineNdots` to `smallish`"
```

You will want to edit a few more places that still have `lineNdots` in them. Type the following to see where all these files are:
```
git grep lineNdots
```

You can replace `lineNdots` for `smallish` quickly with:
```
git grep -l 'lineNdots' | xargs sed -i 's/lineNdots/smallish/g'
```

Edit `lineNdots/__init__.py`, and `lineNdots/version.py` with the information specific to your project.

This very file (`README.md`) should be edited to reflect what your project is about.

At this point, make another commit, and continue to develop your own code based on this template.