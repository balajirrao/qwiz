import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = sql.ext.declarative.declarative_base()
metadata = Base.metadata

questions_correct_answers = sql.Table("questions_correct_answers", metadata,
		sql.Column("question_id", sql.ForeignKey("questions.id")),
		sql.Column("answer_id", sql.ForeignKey("answers.id")))

questions_wrong_answers = sql.Table("questions_wrong_answers", metadata,
		sql.Column("question_id", sql.ForeignKey("questions.id")),
		sql.Column("answer_id", sql.ForeignKey("answers.id")))

class Question(Base) :
	__tablename__ = "questions"

	id = sql.Column(sql.Integer, primary_key=True)
	marks = sql.Column(sql.Integer)
	unit = sql.Column(sql.Integer)
	page = sql.Column(sql.Integer)
	question = sql.Column(sql.Integer)

	#many-to-many relationships
	correct_answers = sql.orm.relationship("Answer", secondary=questions_correct_answers)
	wrong_answers = sql.orm.relationship("Answer", secondary=questions_wrong_answers)

	def __repr__(self) :
		return "<Question %d Marks %d:%d %s>" % (self.marks, self.unit, self.page, self.question)

class Answer(Base) :
	__tablename__ = "answers"

	id = sql.Column(sql.Integer, primary_key=True)
	answer = sql.Column(sql.String, nullable=False, unique=True)

	def __init__(self, answer) :
		self.answer = answer

	def __repr__(self) :
		return "<Answer %s>" % (self.answer)

class QuestionBank(object):
	
	def get_or_create_answers(self, answers) :
		return_answers = list()
		for answer in answers :
			q = self.session.query(Answer).filter_by(answer = answer)
			print q.count()
			if q.count() > 0 :
				return_answers.append(q.first())
			else :
				return_answers.append(Answer(answer))

		return return_answers

	def commit(self) :
		self.session.commit()

	def rollback(self):
		self.session.rollback()

	def add(self, q) :
		self.session.add(q)
	
	def delete_question(self, q) :
		self.session.delete(q)

	def query(self, id = None, marks = None, unit = None, page = None, question = None) :
		self.session.query(Question).filter_by(id = id,
				marks = marks, unit = unit, page = page,
				question = question)

	def __init__(self, filename) :
		self.engine = sql.create_engine("sqlite:///%s" % filename)
		metadata.create_all(self.engine)

		self.session = sql.orm.sessionmaker(bind = self.engine)()
	

#correct_answers = get_or_create_answers(session, ["Kapil",])
#wrong_answers = get_or_create_answers(session, ["Laxman", "Ganguly", "Sachin"])
#question = Question(1, 1, 1, "Who is the DEMI GOD of cricket ?", -1, correct_answers, wrong_answers)
#session.add(question)

#correct_answers = get_or_create_answers(session, ["Sachin",])
#wrong_answers = get_or_create_answers(session, ["Sachin", "Laxman", "Ganguly"])
#question = Question(1, 1, 1, "Who is the GOD of cricket ?", -1, correct_answers, wrong_answers)
#session.add(question)

#session.commit()

#q = session.query(Question).filter_by(marks = 1).first()
#print q.wrong_answers
