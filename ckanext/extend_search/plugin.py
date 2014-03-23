import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import Package, Activity
import ckan.model.meta as meta
import datetime as date
import itertools as itertools


# def check_activity_streams_enabled():
#     # NOTE about the recording of activities...
#     # It is possible to configure CKAN to not record activities (i.e. in the 'activity' table in the DB). If you look in the .ini file, there is a setting:
#     # #ckan.activity_streams_enabled = false
#     # It is commented-out and defaults to 'true' anyway so someone has to explicitly change this setting to disable the logging of activities in the DB.
#     # That said, this extension should check that the setting is 'true' when it gets installed. Otherwise it should bail-out immediately and print something to the logger.
#
#     return "Check .ini config file setting on install of extension"

#Returns custodian field for the Dataset/Package
def custodian():

    #custodian = action.get.user_show({'id':'0b6205c0-3003-4065-80c7-cfefa78be0fc'})
    custodian = "John Citizen"

    return custodian

#Returns Activity datetime for the Dataset/Package
def datetime(pkg_id):

    datetime = "asdf"

    return datetime

'''
Filter activities by date range. Returns activities
'''
def filter_by_date(activities, date_min, date_max):

    _date_min = None
    _date_max = None

    if(date_min):
        _date_min = date_min
    else:
        _date_min = date.datetime(1901,01,01)

    if(date_max):
        _date_max = date_max
    else:
        _date_max = date.datetime.now()

    activities_filtered = itertools.ifilter(lambda x: x.activity_type == 'new package', activities)
    activities_filtered = itertools.ifilter(lambda x: x.timestamp >= _date_min, activities_filtered)
    activities_filtered = itertools.ifilter(lambda x: x.timestamp <= _date_max, activities_filtered)

    return activities_filtered

class ExtendSearchPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''Extends the Ckan dataset/package search

    '''
    #self.before_search({'name':'bananas'})

    activities = meta.Session.query(Activity).all()

   # print([p.object_id for p in activities])

    activities_filtered = filter_by_date(activities, None, None)

   # print([a.object_id for a in activities_filtered])

    packages = []
    for a in activities_filtered:
        package = meta.Session.query(Package).filter(Package.id==a.object_id).first()

        if(package):
            packages.append(package)

    if(packages):
        print([p.name for p in packages])

    # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers, inherit=True)

    # Declare that this class implements IDataSetForm
    plugins.implements(plugins.IDatasetForm, inherit=True)

    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer, inherit=True)

    plugins.implements(plugins.interfaces.IPackageController, inherit=True)



    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')


    def get_helpers(self):
        '''Register the functions above as a template
        helper functions.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {
            'extend_search_custodian': custodian,
            'extend_search_datetime': datetime
             }


    def before_search(self, search_params):
        print search_params

        #Attach our custom search fields
        # - Custodian
        # - Date/DateRange

        return search_params


    # def after_search(*search_results, **search_params):
    #     print search_results
    #     #print search_params

    #    return ({'count': '2','results': search_results, 'facets': 'test'})

    # def package_form(self):
    #     return 'package/new_package_form.html'
    #
    # def new_template(self):
    #     return 'package/new.html'
    #
    # def comments_template(self):
    #     return 'package/comments.html'
    #
    # def search_template(self):
    #     return 'package/search.html'
    #
    # def read_template(self):
    #     return 'package/read.html'
    #
    # def history_template(self):
    #     return 'package/history.html'

    #Required to implement IDatasetForm
    def package_types(self):
        return ['dataset']

    #Required to implement IDatasetForm
    def is_fallback(self):
        return False

    def setup_template_variables(self, context, data_dict=None, package_type=None):
        from ckan.lib.base import c
        from ckan import model
        c.licences = model.Package.get_license_options()

    def _modify_package_schema(self, schema):
        schema.update({
            'custodian': [toolkit.get_validator('ignore_missing'),
                          toolkit.get_converter('convert_to_tags')('custodian')
            ]
        })
        return  schema

    #Schema to use when creating a Dataset
    def create_package_schema(self):
        schema = super(ExtendSearchPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return  schema

    #Schema to use when updating a Dataset
    def update_package_schema(self):
        schema = super(ExtendSearchPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return  schema

    def show_package_schema(self):
         schema = super(ExtendSearchPlugin, self).show_package_schema()

         schema.update({
             'custodian': [toolkit.get_validator('ignore_missing'),
                          toolkit.get_converter('convert_to_tags')('custodian')
             ]
         })
         schema.update({
             'datetime': [toolkit.get_validator('ignore_missing'),
                          toolkit.get_converter('convert_to_tags')('datetime')
             ]
         })


