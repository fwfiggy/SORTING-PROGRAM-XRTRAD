This project is to show handling in data processing and showcases skills in file handling, data manipulation, and generating reports in a structured and automated manner.
This Python application reads the data from 3 output files then uses said data to produce 2 output files. The code is written for python 3. Attached are 5 files used for this project. To run this application, have all 3 input files (TeamMap.csv, ProductMaster.csv, and Sales.csv) along with report.PY in the same directory and that the CSV files are in correct format. Then, in your terminal, run this command:
“python3 report.PY -t TeamMap.csv -p ProductMaster.csv -s Sales.csv --team-report=TeamReport.csv --product-report=ProductReport.csv”


Output: This application will create two CSV files. The first is “TeamReport.csv”, which shows the gross revenue for each team. The second is “ProductReport.csv”, which contains the total units sold, gross revenue, and discount for each respective product.


Quick Troubleshooting
Ensure you are using python 3
CSV files are correctly formatted
Files exist in the correct locations
Required Python modules: csv, argparse, and collections

