import sys, os
from pip.commands.install import InstallCommand
from pip.index import PackageFinder
from pip.req import (InstallRequirement, RequirementSet, parse_requirements,
                     PIP_DELETE_MARKER_FILENAME)
from pip.log import logger
from pip import call_subprocess

class Requisite(InstallCommand):
  name = 'requisite'
  usage = '%prog [OPTIONS]'
  summary = 'Uploads required packages to a PyPI server'
  _ignore = [PIP_DELETE_MARKER_FILENAME]
  
  def __init__(self):
    super(Requisite, self).__init__()
    self.parser.add_option(
      '--cache-dir',
      dest='req_cache_dir',
      default='req_cache',
      metavar='DIR',
      help='Download and extract all packages into a cache directory '
           'it can stick around if that is useful.')
    self.parser.add_option(
      '--repository',
      dest='req_repository',
      default=None,
      metavar='NAME',
      help='Upload to this PyPI repository (it must be present in your ~/.pypirc file)')
    self.parser.add_option(
      '--clean-cache',
      dest='req_clean_cache',
      default=False,
      action='store_true',
      help='Clear cache files after complete operation')
    self.parser.add_option(
      '--req-requirements',
      dest='req_req_requirements',
      default='req-requirements.txt',
      help='File where all the new requirements will be written (this is useful'
      ' because it removes all dependencies on git, since you no longer use it)')
    self.parser.add_option(
      '--no-upload',
      dest='req_no_upload',
      default=False,
      action='store_true',
      help='Will preform all actions without uploading')
  
  
  def _build_package_finder(self, options, index_urls):
    return PackageFinder(find_links=options.find_links, index_urls=index_urls)
  
  def _individual_packages(self, options):
    c_dir = os.path.abspath(options.req_cache_dir)
    for n in os.listdir(c_dir):
      if n not in self._ignore:
        yield os.path.join(c_dir, n)
  
  def repository_url(self, options):
    if not getattr(self, '_repo_url', None):
      from ConfigParser import ConfigParser
      y = ConfigParser()
      y.read(os.path.expanduser('~/.pypirc'))
      setattr(self, '_repo_url', y.get(options.req_repository, 'repository'))
    return self._repo_url
  
  def upload_to_repository(self, options):
    current = os.path.abspath(os.curdir)
    opts = ['sdist', 'register', '-r', options.req_repository, 
            'upload', '-r', options.req_repository]
    setup = ' '.join(['setup.py'] + opts)
    logger.notify('Running %s for packages in %s' % (setup, options.req_cache_dir))
    pkgs = self._individual_packages(options)
    logger.indent += 2
    for n in pkgs:
      os.chdir(n)
      call_subprocess([sys.executable, 'setup.py'] + opts)
    os.chdir(current)
    logger.indent -= 2
  
  def run(self, options, args):
    if not options.req_repository:
      logger.notify('You need to specify a repository. This utility '
                    'does not upload to PyPI')
      return 1
    options.build_dir = os.path.abspath(options.req_cache_dir)
    options.src_dir = os.path.abspath(options.req_cache_dir)
    options.no_install = True
    options.ignore_installed = True
    install_options = options.install_options or []
    global_options = options.global_options or []
    index_urls = [options.index_url] + options.extra_index_urls
    if options.no_index:
      logger.notify('Ignoring indexes: %s' % ','.join(index_urls))
      index_urls = []
    
    finder = self._build_package_finder(options, index_urls)
    
    requirement_set = RequirementSet(build_dir=options.build_dir,
                                     src_dir=options.src_dir,
                                     download_dir=options.download_dir,
                                     download_cache=options.download_cache,
                                     upgrade=options.upgrade,
                                     ignore_installed=options.ignore_installed,
                                     ignore_dependencies=options.ignore_dependencies)
    
    req_req = open(os.path.abspath(options.req_req_requirements), 'w')
    req_req.writelines(['--index-url=%s' % self.repository_url(options), '\n'])
    
    try:
      for filename in options.requirements:
        for req in parse_requirements(filename, finder=finder, options=options):
          logger.info('req ' + str(req.req))
          req_req.writelines([str(req.req), '\n'])
          requirement_set.add_requirement(req)
    finally:
      req_req.close()

    if not options.no_download:
      requirement_set.prepare_files(finder, force_root_egg_info=False, bundle=False)
    else:
      requirement_set.locate_files()
    
    if not os.path.exists(os.path.abspath(options.req_cache_dir)):
      os.mkdir(os.path.abspath(options.req_cache_dir))
    
    if not options.req_no_upload:
      self.upload_to_repository(options)
    
    if options.req_clean_cache:
      requirement_set.cleanup_files(bundle=False)
    
    return requirement_set

Requisite()
