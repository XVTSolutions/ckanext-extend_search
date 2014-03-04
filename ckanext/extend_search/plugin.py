import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

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

    custodian = "John"

    return custodian

#Returns Activity datetime for the Dataset/Package
def datetime():

    datetime = "01/01/2014 12:00pm"

    return datetime


class ExtendSearchPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''Extends the Ckan dataset/package search

    '''
    # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers, inherit=True)

    # Declare that this class implements IDataSetForm
    plugins.implements(plugins.IDatasetForm, inherit=True)

    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer, inherit=True)


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
        return True

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



    # def form_to_db_schema(self, package_type=None):
    #     from ckan.logic.schema import package_form_schema
    #     from ckan.lib.navl.validators import ignore_missing
    #     from ckan.logic.converters import convert_to_tags
    #
    #     schema = package_form_schema()
    #     # schema.update({
    #     #     'custodian': [ignore_missing, convert_to_tags('country_codes')]
    #     # })
    #     return schema
    #
    # def db_to_form_schema(data, package_type=None):
    #     from ckan.logic.schema import package_form_schema
    #     from ckan.logic.converters import convert_from_tags, free_tags_only
    #     from ckan.lib.navl.validators import ignore_missing, keep_extras
    #
    #     schema = package_form_schema()
    #     # schema.update({
    #     #     'tags': {
    #     #         '__extras': [keep_extras, free_tags_only]
    #     #     },
    #     #     'geographical_coverage': [convert_from_tags('country_codes'), ignore_missing],
    #     # })
    #     return schema
