# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'University'
        db.create_table(u'lecture_university', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'lecture', ['University'])

        # Adding model 'Course'
        db.create_table(u'lecture_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('prerequsites', self.gf('django.db.models.fields.TextField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'lecture', ['Course'])

        # Adding model 'Lecturer'
        db.create_table(u'lecture_lecturer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='lecturers', null=True, to=orm['lecture.University'])),
        ))
        db.send_create_signal(u'lecture', ['Lecturer'])

        # Adding M2M table for field courses on 'Lecturer'
        db.create_table(u'lecture_lecturer_courses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lecturer', models.ForeignKey(orm[u'lecture.lecturer'], null=False)),
            ('course', models.ForeignKey(orm[u'lecture.course'], null=False))
        ))
        db.create_unique(u'lecture_lecturer_courses', ['lecturer_id', 'course_id'])

        # Adding model 'Student'
        db.create_table(u'lecture_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('university', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lecture.University'])),
            ('curriculum', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('group_abbrev', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'lecture', ['Student'])

        # Adding model 'Lecture'
        db.create_table(u'lecture_lecture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(related_name='courses', to=orm['lecture.Course'])),
            ('number', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('basic_concepts', self.gf('django.db.models.fields.CharField')(max_length=300, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'lecture', ['Lecture'])

        # Adding M2M table for field designers on 'Lecture'
        db.create_table(u'lecture_lecture_designers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lecture', models.ForeignKey(orm[u'lecture.lecture'], null=False)),
            ('student', models.ForeignKey(orm[u'lecture.student'], null=False))
        ))
        db.create_unique(u'lecture_lecture_designers', ['lecture_id', 'student_id'])


    def backwards(self, orm):
        
        # Deleting model 'University'
        db.delete_table(u'lecture_university')

        # Deleting model 'Course'
        db.delete_table(u'lecture_course')

        # Deleting model 'Lecturer'
        db.delete_table(u'lecture_lecturer')

        # Removing M2M table for field courses on 'Lecturer'
        db.delete_table('lecture_lecturer_courses')

        # Deleting model 'Student'
        db.delete_table(u'lecture_student')

        # Deleting model 'Lecture'
        db.delete_table(u'lecture_lecture')

        # Removing M2M table for field designers on 'Lecture'
        db.delete_table('lecture_lecture_designers')


    models = {
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
        u'lecture.lecturer': {
            'Meta': {'ordering': "('full_name',)", 'object_name': 'Lecturer'},
            'courses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['lecture.Course']", 'null': 'True', 'blank': 'True'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'university': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lecturers'", 'null': 'True', 'to': u"orm['lecture.University']"})
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

    complete_apps = ['lecture']
