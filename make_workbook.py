from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter
import csv

cats=["Fruits & Vegetables","Dairy & Eggs","Snacks & Beverages","Personal Care","Household Essentials","Bakery"]
targets={"Fruits & Vegetables":12000,"Dairy & Eggs":16500,"Snacks & Beverages":13000,"Personal Care":15500,"Household Essentials":17000,"Bakery":12000}

wb=Workbook()
ws=wb.active; ws.title='Monthly Data'
with open('monthly_category_revenue.csv',newline='') as f:
    for row in csv.reader(f): ws.append(row)
for cell in ws[1]: cell.font=Font(bold=True); cell.fill=PatternFill('solid', fgColor='D9EAF7')
ws.freeze_panes='A2'; ws.auto_filter.ref=ws.dimensions

ct=wb.create_sheet('Category Targets'); ct.append(['category','target_revenue_inr'])
for c in cats: ct.append([c,targets[c]])
for cell in ct[1]: cell.font=Font(bold=True); cell.fill=PatternFill('solid', fgColor='D9EAF7')

pt=wb.create_sheet('Pivot Table')
pt.append(['category','SUM of total_revenue','SUM of order_count'])
for i,c in enumerate(cats,2):
    pt.cell(i,1,c)
    pt.cell(i,2,f'=SUMIF(\'Monthly Data\'!$A$2:$A$37,A{i},\'Monthly Data\'!$D$2:$D$37)')
    pt.cell(i,3,f'=SUMIF(\'Monthly Data\'!$A$2:$A$37,A{i},\'Monthly Data\'!$C$2:$C$37)')
for cell in pt[1]: cell.font=Font(bold=True); cell.fill=PatternFill('solid', fgColor='D9EAF7')
pt['A9']='Grand Total'; pt['B9']='=SUM(B2:B7)'; pt['C9']='=SUM(C2:C7)'
for cell in pt[9]: cell.font=Font(bold=True)
pt['E1']='Pivot definition'; pt['E2']='This summary reproduces the required pivot: category in Rows, SUM(total_revenue) and SUM(order_count) in Values, using the unmodified Monthly Data import.'

cs=wb.create_sheet('Category Summary')
headers=['category','Pivot total revenue','target_revenue_inr','variance','percentage_variance','target_status','Matches Part 1 SQL total?']
cs.append(headers)
for cell in cs[1]: cell.font=Font(bold=True); cell.fill=PatternFill('solid', fgColor='D9EAF7'); cell.alignment=Alignment(wrap_text=True)
for r,c in enumerate(cats,2):
    cs.cell(r,1,c)
    cs.cell(r,2,f'=\'Pivot Table\'!B{r}')
    cs.cell(r,3,f'=XLOOKUP(A{r},\'Category Targets\'!$A$2:$A$7,\'Category Targets\'!$B$2:$B$7,"Not Found")')
    cs.cell(r,4,f'=C{r}-B{r}')
    cs.cell(r,5,f'=((B{r}-C{r})/C{r})*100')
    cs.cell(r,6,f'=IF(B{r}>=C{r},"Above Target",IF((C{r}-B{r})<=0.15*C{r},"Below Target - Watch","Below Target - Critical"))')
    cs.cell(r,7,f'=IF(B{r}=C{r},"Yes","No")')
# Replace matches formulas with explicit comparison to Part 1 expected SQL values, as a manual reconciliation aid.
expected={"Fruits & Vegetables":9790,"Dairy & Eggs":14090,"Snacks & Beverages":10895,"Personal Care":16382,"Household Essentials":21715,"Bakery":15410}
for r,c in enumerate(cats,2): cs.cell(r,7,f'=IF(B{r}={expected[c]},"Yes","No")')
for r in range(2,8):
    cs.cell(r,2).number_format='#,##0'; cs.cell(r,3).number_format='#,##0'; cs.cell(r,4).number_format='#,##0'; cs.cell(r,5).number_format='0.00'
cs.conditional_formatting.add('F2:F7', FormulaRule(formula=['F2="Above Target"'], fill=PatternFill('solid', fgColor='C6EFCE')))
cs.conditional_formatting.add('F2:F7', FormulaRule(formula=['F2="Below Target - Watch"'], fill=PatternFill('solid', fgColor='FFEB9C')))
cs.conditional_formatting.add('F2:F7', FormulaRule(formula=['F2="Below Target - Critical"'], fill=PatternFill('solid', fgColor='FFC7CE')))

for sheet in wb.worksheets:
    for col in range(1, sheet.max_column+1):
        vals=[str(sheet.cell(r,col).value or '') for r in range(1,min(sheet.max_row,40)+1)]
        width=min(max(len(v) for v in vals)+2,42)
        sheet.column_dimensions[get_column_letter(col)].width=width
    sheet.freeze_panes = sheet.freeze_panes or 'A2'

wb.save('bigbasket_category_analysis.xlsx')
