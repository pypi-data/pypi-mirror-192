from setuptools import setup, find_packages
  
with open('requirements.txt') as f:
    requirements = f.readlines()
  
long_description = 'POC in command line packages using python'
  
setup(
        name ='devopspipelinepoc',
        version ='0.1.7',
        author ='Puneet Udhayan',
        author_email ='puneetudhayan@gmail.com',
        url ='https://github.com/PuneetUdhayanGraphene/devops-pipeline-poc',
        description ='POC in command line packages using python',
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        packages = find_packages(),
        entry_points ={
            'console_scripts': [
                'devopspipelinepoc = devopspipelinepoc.main:app'
            ]
        },
        classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ),
        keywords ='python package',
        install_requires = requirements,
        package_data={'devopspipelinepoc': ['data/*.txt']},
        zip_safe = False
)