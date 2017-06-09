# coding=utf-8
__author__ = 'yyx'
__date__ = '2017/5/22 16:48'

import xadmin

from .models import UserAsk, UserCourse, UserMessage, CourseComments, UserFaverite


class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'courses', 'add_time']
    search_fields = ['user', 'courses']
    list_filter = ['user', 'courses', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'add_time', 'has_read']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'add_time', 'has_read']


class UserComments(object):
    list_display = ['user', 'courses', 'comments', 'add_time']
    search_fields = ['user', 'courses', 'comments']
    list_filter = ['user', 'courses', 'comments', 'add_time']


class UserFaveriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'courses', 'comments', 'add_time']
    search_fields = ['user', 'courses', 'comments']
    list_filter = ['user', 'courses', 'comments', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserFaverite, UserFaveriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)