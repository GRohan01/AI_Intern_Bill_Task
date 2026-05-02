Light Bill Data Extractor :



This project is a simple web application built using Streamlit. It reads electricity bill PDFs and extracts important information like consumer name, consumer number, units, and total amount.

The system works for both English and Marathi bills.





How the project works:



First, the user uploads a light bill PDF.

The system converts the PDF into images.

Then it uses OCR to read text from the images.

After that, it searches for important values using keywords.

If the consumer name is not found using keywords, the system uses a fallback method. It finds the mobile number and takes the next line as the consumer name.

Finally, the extracted data is shown on the screen and saved into an Excel file.





Features :



Supports English and Marathi language

Extracts consumer name, number, units, and amount

Handles cases where consumer name is not labeled

Saves extracted data into Excel file automatically

Works with multi-page PDFs





Project Structure:



app.py is the main file which runs the application

tessdata folder contains language files for OCR

Extract\_Data.xlsx stores all extracted results





How to run the project:



Step 1: Install required libraries using pip install -r requirements.txt

Step 2: Install Tesseract OCR on your system

Step 3: Download eng.traineddata and mar.traineddata and place them inside tessdata folder

Step 4: Update the Tesseract path in the code if needed

Step 5: Run the application using streamlit run app.py

Step 6: Upload a light bill PDF and see the results





Output :



The extracted data will be shown in the app

The same data will be saved in Extract\_Data.xlsx file in the project folder

