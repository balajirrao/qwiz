#!/usr/bin/python

import sys
try:
	import pygtk
	pygtk.require("2.0")
except:
	pass

try:
	import gtk
	import gtkspell
except:
	sys.exit(1)

import QuestionBank as QB

class Application(object):
	def get_ui_object(self, name) :
		return self.builder.get_object(name)

	def load(qb_filename) :
		self.qb = QB.QuestionBank(qb_filename)

	def window_destroy(self, widget, data=None) :
		gtk.main_quit()
	
	def new_q(self, widget) :
		pass
		# Setup textview focus out handlers

		self.vbox_q.set_sensitive(True)
		self.q = QB.Question()
		self.qb.add(self.q)

	def linked_q(self) :
		pass

	def edit_q(self) :
		pass

	def copy_q(self) :
		pass
#
	def delete_q(self, widget) :
		self.commit_q()
		pass

	def commit_q(self) :
		# Only question and answers are to be updated.
		
		# Marks
		for radio, mark in self.radios :
			if radio.get_active() :
				self.mark = mark

		# Unit and Page
		self.q.unit = int(self.entry_unit.get_text())
		self.q.page = int(self.entry_page.get_text())
	
		def get_text_from_textbuffer(textbuffer) :
			start = textbuffer.get_start_iter()
			end = textbuffer.get_end_iter()
			text = textbuffer.get_text(start, end);
			if len(text) != 0 :
				return text
			else :
				return None

		correct_answers = list()
		wrong_answers = list()
		for k,v in self.textbuffer_answers.items() :
			l = locals()["%s_answers" % k]
			for buffer in v :
				text = get_text_from_textbuffer(buffer)
				if (text is not None) :
					l.append(text)

			answers = getattr(self.q, "%s_answers" % k)
			del answers[:]
			answers += self.qb.get_or_create_answers(l)

		self.qb.commit()
	
	def rollback_q(self) :
		self.qb.rollback()

	def __init__(self) :
		self.builder = gtk.Builder()
		self.builder.add_from_file("gui.glade")

		# Setup spell check
		self.textview_q = self.get_ui_object("textview_question")
		gtkspell.Spell(self.textview_q)

		# Setup question text buffer
		self.textbuffer_q = self.get_ui_object("textbuffer_question")

		# Setup answer text buffers
		self.textbuffer_answers = {"correct" : list(), "wrong" : list()}
		for k,v in self.textbuffer_answers.items() :
			i = 1
			while i >= 0 :
				buffer = self.get_ui_object("textbuffer_%s_%d" % (k, i))
				if (buffer is None) :
					break;

				v.append(buffer)
				i += 1

		# Setup marks radios
		self.radios = [(self.get_ui_object("radiobutton_mark_1"), 1),
				(self.get_ui_object("radiobutton_mark_2"), 2),
				(self.get_ui_object("radiobutton_mark_4"), 4),]

		# Setup page and unit entries
		self.entry_page = self.get_ui_object("entry_page")
		self.entry_unit = self.get_ui_object("entry_unit")

		# Set signal handlers for toolbar buttons
		actions = ["new", "linked", "copy", "edit", "delete"]
		for action in actions :
			widget = self.get_ui_object("toolbutton_%s" % action)
			widget.connect("clicked", getattr(self, "%s_q" % action))
		
		# Get reference to question vbox for setting it's sensitivity
		self.vbox_q = self.get_ui_object("vbox_question")

		# Setup QuestionBank
		self.qb = QB.QuestionBank("qbank.db")
		self.q = None

		# Populate the TreeView
		self.treestore = self.get_ui_object("treestore_questions")

	
		# Setup window
		self.window = self.get_ui_object("main_window")
		if(self.window) :
			self.window.connect("destroy", self.window_destroy)
	
		self.window.maximize()
		self.window.show()

	def run(self) :
		gtk.main()

if __name__ == "__main__" :
	app = Application()
	app.run()
