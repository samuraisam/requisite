import sys, os
from pip.commands.install import InstallCommand
from pip.index import PackageFinder
from pip.req import InstallRequirement, RequirementSet, parse_requirements
from pip.log import logger
from pip import call_subprocess

class Requisite(InstallCommand):
  name = 'requisite'
  usage = '%prog [OPTIONS]'
  summary = 'Uploads required packages to a PyPI server'
  
  def __init__(self):
    super(Requisite, self).__init__()
    self.parser.add_option(
      '--cache-dir',
      dest='req_cache_dir',
      default='req_cache',
      metavar='DIR',
      help='Download and extract all packages here'
    )
    self.parser.add_option(
      '--repository',
      dest='req_repository',
      default=None,
      metavar='URL',
      help='Upload to this PyPI repository'
    )
    self.parser.add_option(
      '--clean-cache',
      dest='req_clean_cache',
      default=False,
      action='store_true',
      help='Whether or not to save cache files '
           '(it will be faster to save these)'
    )
  
  def _build_package_finder(self, options, index_urls):
    return PackageFinder(find_links=options.find_links, index_urls=index_urls)
  
  def _individual_packages(self):
    return []
  
  def _upload_to_repository(self):
    pass
  
  def run(self, options, args):
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
    
    for filename in options.requirements:
      for req in parse_requirements(filename, finder=finder, options=options):
        print 'req', req
        requirement_set.add_requirement(req)

    if not options.no_download:
      requirement_set.prepare_files(finder, force_root_egg_info=self.bundle, bundle=self.bundle)
    else:
      requirement_set.locate_files()
    
    if options.req_clean_cache:
      requirement_set.cleanup_files(bundle=False)
    
    return requirement_set

Requisite()
