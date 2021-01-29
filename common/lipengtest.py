# from keras.utils.data_utils import get_file
# from tensorflow.keras.utils import get_file
# import zipfile
# import os
#
# file = 'data.zip'
# dir = 'D:\pythonProject'
# url = "http://cdnoss.stardustgod.com/avgContent-test/gamecfg_0805test_20201217_Q5yEz1.zip"
#
# os.chdir(dir)
# try:
#     path = get_file(fname=file,
#                     origin=url, cache_subdir=dir)  #
# except:
#     print('Error')
#     raise
# def un_zip(file_name):
#
#     zip_file = zipfile.ZipFile(file_name)
#     for names in zip_file.namelist():
#         zip_file.extract(names)
#     zip_file.close()
# un_zip(file)