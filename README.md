# hand-written-digit-barcode-generator

### Step 1
> clone the repository
> ```shell
> git clone https://github.com/ahmetkca/hand-written-digit-barcode-generator.git
> ```

### Step 2
> First create a python virtual environment
> ```bash
> py -m venv .venv
> ```

### Step 3
> After you created the venv you need to activate it
>
> on Powershell
> ```bash
> .\.venv\Scripts\Activate.ps1
> ```
>
> on Command Prompt
> ```bash
> .venv\Scripts\activate.bat
> ```

### Step 4
> You can install all the requirments by typing the following command (you need to activate venv first)
>
> ```bash
> pip install -r requirements.txt
> ```

### Step 5
> You can configure the constants.py file before running the run.bat
> 
> After you configured you can run the run.bat by
> 
> on Powershell
> ```bash
> .\run.bat
> ```
> 
> on Command Prompt
> ```bash
> run.bat
> ```

### Step 6
> run.bat file will create thresholds.txt and barcodes.txt files
> 
> You can run the program by typing following command on Powershell
> ```bash
> py .\search_similar_image.py
> ```

### Step 7 (Optional)
> Optionally you can create image of barcode by typing following command
> 
> ```bash
> py .\create_barcode_image.py
> ```
> this python file will create image representation of binary barcode
