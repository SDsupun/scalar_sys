from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("advance_setting_page",  ["page/advance_setting_page.py"]),
    Extension("first_page",  ["page/first_page.py"]),
    Extension("login_page",  ["page/login_page.py"]),
    Extension("main_page",  ["page/main_page.py"]),
    Extension("multi_page",  ["page/multi_page.py"]),
    Extension("notification",  ["page/notification.py"]),
    Extension("page_manager",  ["page/page_manager.py"]),
    Extension("print_page",  ["page/print_page.py"]),
    Extension("printer_setting_page",  ["page/printer_setting_page.py"]),
    Extension("profile_setting_page",  ["page/profile_setting_page.py"]),
    Extension("report_page",  ["page/report_page.py"]),
    Extension("scalar_sys_calender",  ["page/scalar_sys_calender.py"]),
    Extension("second_page",  ["page/second_page.py"]),
    Extension("selectableGrid",  ["page/selectableGrid.py"]),
    Extension("sys_popup",  ["page/sys_popup.py"]),
    Extension("reportDoc",  ["sysCom/reportDoc.py"]),
    Extension("scalar_com",  ["sysCom/scalar_com.py"]),
    Extension("ticketDoc",  ["sysCom/ticketDoc.py"]),
]
setup(
    name='Scalar System',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules
)
