import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import User
import ckan.model.meta as meta
from ckan.lib.base import c


class ExtendSearchPlugin(plugins.SingletonPlugin):
    '''Extends the Ckan dataset/package search
    '''
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IDatasetForm, inherit=True)


    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic', 'ckanext-datesearch')


    def before_search(self, search_params):

        extras = search_params.get('extras')
        if not extras:
            # There are no extras in the search params, so do nothing.
            return search_params

        start_date = extras.get('ext_startdate')
        end_date = extras.get('ext_enddate')

        if not start_date or not end_date:
            # The user didn't select a start and end date, so do nothing.
            return search_params

        # Add a date-range query with the selected start and end dates into the
        # Solr facet queries.
        fq = search_params['fq']
        fq = '{fq} +metadata_modified:[{start_date} TO {end_date}]'.format(
            fq=fq, start_date=start_date, end_date=end_date)

        search_params['fq'] = fq

        return search_params

    #IDatasetForm methods
    def package_form(self):
        return 'package/new_package_form.html'

    def new_template(self):
        return 'package/new.html'

    def comments_template(self):
        return 'package/comments.html'

    def search_template(self):
        return 'package/search.html'

    def read_template(self):
        return 'package/read.html'

    def history_template(self):
        return 'package/history.html'

    def package_types(self):
        return ['dataset']

    def is_fallback(self):
        return True

    def setup_template_variables(self, context, data_dict=None, package_type=None):
        c.users = meta.Session.query(User).all()