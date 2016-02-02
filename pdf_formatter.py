#Copyright 2016 Matthew Plitnikas
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


import os
import sys
import subprocess
import re
import shutil

import pdfread
from pypdfocr import pypdfocr


class PDFsorter(object):
	'''
	When pointed to a folder, OCRs the first page of each PDF, and sorts
	according to LASTNAME, TAXYEAR, and SSN(4-digit). Creates a folder named
	[LASTNAME, SSN] and moves the PDF inside, then renames it to TAXYEAR. In
	the case of multiple PDFs for a LASTNAME/SSN combo, moves all associated
	PDFs into that folder.
	'''
	def __init__(self, arg_path):	
		
		self.arg_path = os.path.join(os.getcwd(), arg_path)	

	def get_path(self, path):
		'''Checks whether the working folder is valid.'''
		if os.path.exists(self.arg_path):
			os.chdir(self.arg_path)
			print "Working in folder:"
			print self.arg_path
		else:
			print "Sorry, the specified folder cannot be found:"
			print self.arg_path
			sys.exit()

	def pypdfocr_call(self):
		'''Calls out to pypdfocr via cmd.'''
		item_call = 'pypdfocr %s --skip-preprocess' % self.item
		item_call = item_call.split(' ')
		subprocess.call(item_call)
		self.item_ocr_name = '%s_ocr.pdf' % self.item_bits[0]

	def pdfread_get(self):
		'''Grabs text from pdfread module into variables.'''
		item_info = pdfread.main(self.item_ocr_name)
		self.lastname = item_info['name']
		self.taxyear = item_info['year']
		self.ssn = item_info['ssn']

	def create_folder(self):
		'''Check whether the folder exists. If not, create it.'''
		new_folder_name = self.lastname.upper() + ', ' + self.ssn.upper()
		self.new_folder_path = os.path.join(os.curdir, new_folder_name)
		if not os.path.exists(self.new_folder_path):
			os.mkdir(new_folder_name)

	def move_pdf(self):
		'''Check whether the file is already in place. If not, move + rename it.'''
		orig = self.item
		dest = os.path.join(self.new_folder_path, self.taxyear + '.pdf')
		if not os.path.exists(dest):
			shutil.move(orig, dest)
		else:
			raise Exception


	def folder_handle(self):
		'''Main loop of the PDFsorter. Goes thru every item in the directory.'''
		folder_contents = os.listdir(os.curdir)

		# can we make this a generator?
		for self.item in folder_contents:
			self.item_bits = self.item.split('.')
			
			if self.item_bits[-1] == 'pdf':
				
				# convert the pdf
				print "Converting PDF. This may take a moment..."
				self.pypdfocr_call()
				
				# open using pdfread:
				print "Extracting PDF text"
				try:
					self.pdfread_get()
				except:
					# if we can't read the pdf, just keep going
					print "Couldn't read the PDF. Skipping."
					continue
				
				# using the info, create folder
				print "Creating folder"
				self.create_folder()

				# delete OCR file
				print "Cleaning up temp file"
				os.remove(self.item_ocr_name)

				print "Moving PDF to its new folder"
				try:
					self.move_pdf()
				except:
					print "ERROR: That file already exists: " + self.item + ". Skipping."
					continue

				print "Done!"
					
	def go(self):
		'''
		Main entry point for pdf_formatter. Hands off to
		folder_handle for the looping function.
		'''
		self.get_path(self.arg_path)

		# Main loop
		self.folder_handle()

def main():
	arg_path = ' '.join(sys.argv[1:])
	blah = PDFsorter(arg_path)	
	blah.go()

if __name__ == '__main__':
	main()