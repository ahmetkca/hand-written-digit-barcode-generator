# hand-written-digit-barcode-generator

[Project Report](Data_Structures_Project_Report.pdf)

### Step 1
> clone the repository
> ```
> git clone https://github.com/ahmetkca/hand-written-digit-barcode-generator.git
> ```

### Step 2
> First create a python virtual environment
> ```
> py -m venv .venv
> ```

### Step 3
> After you created the venv you need to activate it
>
> on Powershell
> ```
> .\.venv\Scripts\Activate.ps1
> ```
>
> on Command Prompt
> ```
> .venv\Scripts\activate.bat
> ```

### Step 4
> You can install all the requirments by typing the following command (you need to activate venv first)
>
> ```
> pip install -r requirements.txt
> ```

### Step 5
> You can configure the constants.py file before running the run.bat
> 
> After you configured you can run the run.bat by
> 
> on Powershell
> ```
> .\run.bat
> ```
> 
> on Command Prompt
> ```
> run.bat
> ```

### Step 6
> run.bat file will create thresholds.txt and barcodes.txt files
> 
> You can run the program by typing following command on Powershell
> ```
> py .\search_similar_image.py
> ```

### Step 7 (Optional)
> Optionally you can create image of barcode by typing following command
> 
> ```
> py .\create_barcode_image.py
> ```
> this python file will create image representation of binary barcode
