from setuptools import setup

setup(name="imputing_final",
      version="0.0.3",
      url="https://github.com/waikoreaweatherpjt/imputing_final",
      licence="MIT",
      author="wai kimsanghyun",
      author_email="waik@waikorea.com",
      keywords=["imputing","numpy","coulmnwise"],
      description="imputing with numpy no loop",
      py_modules=["imputing_final"],
      install_requires=["numpy","pandas"]
      )