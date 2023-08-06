from setuptools import setup, find_packages

setup(
    name='cntm',
    version='0.0.1',
    author='Hamed Rahimi',
    author_email='<hamed.rahimi@sorbonne-universite.fr',
    description='Citation-informed Neural Topic Models',
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    url='https://github.com/hamedR96/CNTM',
    packages=find_packages(),
    install_requires=["pandas","numpy","torch","umap-learn","transformers","torch",
                      "swifter","nltk","gensim","scikit-learn","scipy","rank_bm25"
                      ],
    
    project_urls={
        'Bug Tracker': 'https://github.com/hamedR96/CNTM/issues'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X ",
        "Operating System :: Unix ",
        "Operating System :: Microsoft :: Windows ",
    ],

)
