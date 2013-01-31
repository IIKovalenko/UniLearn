# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LectureTest'
        db.create_table(u'exam_lecturetest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lecture', self.gf('django.db.models.fields.related.OneToOneField')(related_name='test', unique=True, to=orm['lecture.Lecture'])),
        ))
        db.send_create_signal(u'exam', ['LectureTest'])

        # Adding model 'TestQuestion'
        db.create_table(u'exam_testquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(related_name='questions', to=orm['exam.LectureTest'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('type', self.gf('django.db.models.fields.CharField')(default='FV', max_length=2)),
            ('correct_answer_index', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('correct_answer_text', self.gf('django.db.models.fields.CharField')(max_length=511, blank=True)),
            ('difficulty', self.gf('django.db.models.fields.SmallIntegerField')(default=2, max_length=1)),
        ))
        db.send_create_signal(u'exam', ['TestQuestion'])

        # Adding model 'TestQuestionVariant'
        db.create_table(u'exam_testquestionvariant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variants', to=orm['exam.TestQuestion'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=1023)),
            ('number', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal(u'exam', ['TestQuestionVariant'])

    def backwards(self, orm):
        # Deleting model 'LectureTest'
        db.delete_table(u'exam_lecturetest')

        # Deleting model 'TestQuestion'
        db.delete_table(u'exam_testquestion')

        # Deleting model 'TestQuestionVariant'
        db.delete_table(u'exam_testquestionvariant')

    models = {
        u'exam.lecturetest': {
            'Meta': {'object_name': 'LectureTest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'test'", 'unique': 'True', 'to': u"orm['lecture.Lecture']"})
        },
        u'exam.testquestion': {
            'Meta': {'object_name': 'TestQuestion'},
            'correct_answer_index': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'correct_answer_text': ('django.db.models.fields.CharField', [], {'max_length': '511', 'blank': 'True'}),
            'difficulty': ('django.db.models.fields.SmallIntegerField', [], {'default': '2', 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1023'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'to': u"orm['exam.LectureTest']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'FV'", 'max_length': '2'})
        },
        u'exam.testquestionvariant': {
            'Meta': {'ordering': "('question', 'number')", 'object_name': 'TestQuestionVariant'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.SmallIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variants'", 'to': u"orm['exam.TestQuestion']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '1023'})
        },
        u'lecture.course': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Course'},
            'abbrev': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prerequsites': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'lecture.lecture': {
            'Meta': {'ordering': "('course', 'number')", 'object_name': 'Lecture'},
            'basic_concepts': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'courses'", 'to': u"orm['lecture.Course']"}),
            'designers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lecture.Student']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'lecture.student': {
            'Meta': {'ordering': "('curriculum', 'group_abbrev', 'full_name')", 'object_name': 'Student'},
            'curriculum': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'group_abbrev': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lecture.University']"})
        },
        u'lecture.university': {
            'Meta': {'ordering': "('name',)", 'object_name': 'University'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['exam']