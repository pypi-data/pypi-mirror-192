from distutils.core import setup
setup(
  name = 'mayacv',         # How you named your package folder (MyLib)
  packages = ['mayacv'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This package provideHand package recognision module based on media pipe',   # Give a short description about your library
  author = 'Dilum Darshana',                   # Type in your name
  author_email = 'dilumbandara095@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/dilum95/Maya_CV.git',   # Provide either the link to your github or to your website
  download_url = '',    # I explain this later on
  keywords = ['computer vision','pose recognision','finger tracking','finger tracking using media pipe'],   # Keywords that define your package best
  install_requires=[ 
       'opencv-python',
       'mediapipe'   
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
