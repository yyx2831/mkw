# coding=utf-8
__author__ = 'yyx'
__date__ = '2017/5/18 17:41'

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner


class BaseSetting(object):
    enable_themes = True        # 打开主题设置选项
    use_bootswatch = True       # 注入自带的主题


class GlobalSetting(object):
    site_title = "慕学后台管理系统"      # 修改左上角django xadmin的标题
    site_footer = "慕学在线网"          # 修改页脚©我的公司
    menu_style = "accordion"            # 使菜单可收缩


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']  #
    search_fields = ['code', 'email', 'send_type']  # 搜索字段
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 过滤器
    list_fields = ['code', 'email', 'send_type', 'send_time']  # 按这种格式显示


# 对各个models进行注册
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index' ]  # 搜索字段
    list_filter = ['title', 'image', 'url', 'index', 'add_time']    # 过滤器

# 关联注册
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)