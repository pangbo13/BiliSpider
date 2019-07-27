import setuptools

with open('README.md','r',encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'BiliSpider',
    version = '0.1.2',
    author = 'pangbo',
    author_email = '373108669@qq.com',
    description = 'A spider of Bilibili',
    long_description = long_description ,
    long_description_content_type = 'text/markdown',
    url = r'https://github.com/pangbo13/BiliSpider/',
    packages = setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    entry_points = {'console_scripts': [
        'BiliSpider = BiliSpider.__init__:main',
        ],},
    )
