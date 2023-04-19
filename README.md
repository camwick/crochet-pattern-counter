# Crochet Pattern Counter

This program will count adjacent colors in each row found in a pattern image file. Inside `counterUI.py`, you can change the folder directories where the images can be found and where the counted images will be saved.

The program will first search for any images found in the `images/` (or the specified dir) directory and provide them as options in the combo box. Then, after checking for valid data and filepaths, the image will be overwritten with the counts of adjacent colors found in each row.

## Required Python Packages

- PyQt6
- PIL

## Creating EXE

To create an executable, insure that pyinstaller is istalled with `pip intall pyinstaller`. 
Here is the command used to create the executible: 
```
pyinstaller --onefile --windowed --name "Crochet Color Counter" --add-data="./counterUI.ui;." counterUI.py PatternCounter.py
```

On first run, the executable will create the directories specifed in `counterUI.py`.

~ Note, if on Linux, the `;` in the `--add-data` flag must be changed to a `:`. Refer to the [Pyinstaller Manual](https://pyinstaller.org/en/stable/index.html) for specifics.
