# vuv
vuv is a PyPI application to evaluate the vaccine effects on mortality by age group 
between fully vaccinated and unvaccinated. 
CDC dataset is automatically downloaded from the following site:

https://data.cdc.gov/api/views/3rge-nu2a/rows.csv

Five age groups include 18-29,30-49,50-64,65-79, and 80+. 
Choose one of five age groups and enter the age group with vuv command.

To install vuv, 

$ pip install vuv

To run vuv, enter one of five age groups.

$ vuv 80+

This command generates 80+.png image file.

<img src=https://github.com/ytakefuji/vuv/raw/main/80%2B.png  width=350 height=280>
