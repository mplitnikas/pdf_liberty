
def main(pdf_item):
	'''
	Opens a selected OCR'd pdf file and extracts the necessary info
	from the text.
	Returns the info as a dict with {year/name/ssn}
	'''
	def pdf_go(pdf_item):
		import PyPDF2

		with open(pdf_item, 'rb') as pdfFileObj:
			pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
			
			if not pdfReader.numPages:
				raise Exception(pdf_item + 'has zero pages!')
			
			pageObj = pdfReader.getPage(0)
			return pageObj.extractText()
	
	def regex_go(sample_text):
		import re
	
		year_regex = re.compile(r'Tax\sYear\s(\d{4})', re.MULTILINE)
		name_regex = re.compile(r'[A-Z]+\s([A-Z]+)\sTaxpayer', re.MULTILINE)
		ssn_regex = re.compile(r'\*{3}\-\*{2}\-(\d{4})', re.MULTILINE)
	
		yro = year_regex.search(sample_text)
		nro = name_regex.search(sample_text)
		sro = ssn_regex.search(sample_text)
	
		try:
			year = yro.group(1)
			name = nro.group(1)
			ssn = sro.group(1)
		except:
			print "Missing some info in the text."
			return None
	
		return {'year': year, 'name': name, 'ssn': ssn}
	
	pdf_text = pdf_go(pdf_item)
	info = regex_go(pdf_text)
	
	return info

if __name__ == '__main__':
	main()