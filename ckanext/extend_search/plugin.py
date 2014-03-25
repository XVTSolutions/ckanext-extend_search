import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import User, Package
import ckan.model.meta as meta
from ckan.lib.base import c



class ExtendSearchPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    '''Extends the Ckan dataset/package search
    '''
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)


    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic', 'ckanext-datesearch')
        toolkit.add_resource('fanstatic', 'custodianpicker-module')


    # Add the custom parameters to Solr's facet queries
    def before_search(self, search_params):

        extras = search_params.get('extras')
        if not extras:
            # There are no extras in the search params, so do nothing.
            return search_params

        start_date = extras.get('ext_startdate')
        end_date = extras.get('ext_enddate')
        cust_id = extras.get('ext_cust_id')

        if not cust_id:
            if not start_date or not end_date:
                # The user didn't select any additional params, so do nothing.
                return search_params

        fq = search_params['fq']

        if start_date and end_date:
            # Add a date-range query with the selected start and end dates into the
            # Solr facet queries.
            fq = '{fq} +metadata_modified:[{start_date} TO {end_date}]'.format(
                fq=fq, start_date=start_date, end_date=end_date)

        #Add creator (user) id query to the Solr facet queries
        if cust_id:
            fq = '{fq} +maintainer:{cust_id}'.format(
                fq=fq, cust_id=cust_id)

        #return modified facet queries
        search_params['fq'] = fq

        return search_params


    #IDatasetForm methods
    def package_form(self):
        return super(ExtendSearchPlugin, self).package_form()

    def new_template(self):
        return super(ExtendSearchPlugin, self).new_template()

    def comments_template(self):
        return super(ExtendSearchPlugin, self).comments_template()

    def search_template(self):
        return super(ExtendSearchPlugin, self).search_template()

    def read_template(self):
        return super(ExtendSearchPlugin, self).read_template()

    def history_template(self):
        return super(ExtendSearchPlugin, self).history_template()

    def package_types(self):
        return ['dataset']

    def edit_template(self):
        return super(ExtendSearchPlugin, self).edit_template()

    def is_fallback(self):
        return False


    #Setup the model(s) to use in the template initialisation
    def setup_template_variables(self, context, data_dict=None, package_type=None):
       # c.users = meta.Session.query(User).all()

        packages = meta.Session.query(Package).all()
        maintainers = []

        for p in packages:
            maintainers.append(p.maintainer)

        maintset = set(maintainers)
        c.maintainers = maintset

