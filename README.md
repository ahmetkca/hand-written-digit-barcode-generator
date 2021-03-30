# hand-written-digit-barcode-generator
- - -

First clone the repository
```
git clone https://github.com/ahmetkca/hand-written-digit-barcode-generator.git
```
- - -

Create a python virtual environment inside the cloned repository
```
py -m venv .venv
```
- - -

After you created the venv you need to activate it

on Powershell
```
.\.venv\Scripts\Activate.ps1
```

on Command Prompt
```
.venv\Scripts\activate.bat
```
- - -

You can install all the requirments by typing command line (you need to activate venv first)

```
pip install -r requirements.txt
```
- - -

You can configure the constants.py file before running the run.bat

After you configured you can run the run.bat by

On Powershell
```
.\run.bat
```

On Command Prompt
```
run.bat
```
- - -

run.bat file will create thresholds.txt and barcodes.txt files

You can run the program by typing following command

on Powershell
```
py .\search_similar_image.py
```
- - -

Optionally you can create image of barcode by typing following command

on Powershell
```
py .\create_barcode_image.py
```

this python file will create image representation of binary barcode
