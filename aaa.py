# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import string
import signal
from prompt_toolkit import AbortAction, prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import InMemoryHistory

from pygments.lexers import SqlLexer
from pygments.style import Style
from pygments.styles.default import DefaultStyle
from pygments.token import Token
from cmd import Cmd

sql_completer = WordCompleter(['create', 'select', 'insert', 'drop',
                               'delete', 'from', 'where', 'table'], ignore_case=True)

class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)
	

class CmdTest(Cmd):
	def __init__(self):            #初始基础类方法
		Cmd.__init__(self)
		doc_header = 'Core Commands Menu (help <command> for details)'
		misc_header = 'Miscellaneous help topics:'
		undoc_header = 'No help on following command(s)'
		self.prompt = "> "    # define command prompt
		
	def help_hello(self):
		ch = string.ascii_letters + string.digits + '_'
		print ch
		
	def do_hello(self,line):
		print("do_hello:",line)
	
	def help_exit(self):          #以help_*开头的为帮助
		print("输入exit退出程序")
	
	def do_quit(self,line):
		return True

	def do_q(self,line):
		return True
	
	def handler(signum, frame):
		pass
		
	def do_debug(self, line):
		"""Enter into python debug mode"""
		signal.signal(signal.SIGINT, self.handler)
		import pdb
		debugger = pdb.Pdb()
		debugger.prompt = "Pocsuite-debug-shell> "
		debugger.set_trace()

	def cmdloop(self, intro=None):
		"""Repeatedly issue a prompt, accept input, parse an initial prefix
		off the received input, and dispatch to action methods, passing them
		the remainder of the line as argument.

		"""

		self.preloop()
		if self.use_rawinput and self.completekey:
			try:
				import readline
				self.old_completer = readline.get_completer()
				readline.set_completer(self.complete)
				readline.parse_and_bind(self.completekey+": complete")
			except ImportError:
				pass
		try:
			if intro is not None:
				self.intro = intro
			if self.intro:
				self.stdout.write(str(self.intro)+"\n")
			stop = None
			while not stop:
				if self.cmdqueue:
					line = self.cmdqueue.pop(0)
				else:
					if self.use_rawinput:
						try:
							history = InMemoryHistory()
							line = prompt('> ', lexer=SqlLexer, completer=sql_completer,style=DocumentStyle, history=history,on_abort=AbortAction.RETRY)
						except EOFError:
							line = 'EOF'
					else:
						self.stdout.write(self.prompt)
						self.stdout.flush()
						line = self.stdin.readline()
						if not len(line):
							line = 'EOF'
						else:
							line = line.rstrip('\r\n')
				line = self.precmd(line)
				stop = self.onecmd(line)
				stop = self.postcmd(stop, line)
			self.postloop()
		finally:
			if self.use_rawinput and self.completekey:
				try:
					import readline
					readline.set_completer(self.old_completer)
				except ImportError:
					pass	
					
if __name__ == "__main__":
    cmd=CmdTest()
    cmd.cmdloop("hahaha")

	