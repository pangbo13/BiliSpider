import setuptools

with open('version.txt','r') as f:
    version = f.read()

with open('./bilispider/version.py','w') as f:
    out = r'version = ' + repr(version)
    f.write(out)

with open('README.md','r',encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'bilispider',
    version = version,
    license = 'MIT License',
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
        'BiliSpider = bilispider.__init__:main',
        ],},
    )
