import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import User, Package
import ckan.model.meta as meta
from ckan.lib.base import c
from sqlalchemy import distinct


class ExtendSearchPlugin(plugins.SingletonPlugin):
    '''
    Extends the Ckan dataset/package search
    '''
    print "loading ckanext-extend_search"

    plugins.implements(plugins.IConfigurer)
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


    def after_search(self, search_params, search_results):

        #Return a list of maintainers for the view
#         packages = meta.Session.query(Package).all()
#         maintainers = []
# 
#         for p in packages:
#             if(p.maintainer):
#                 maintainers.append(p.maintainer)

        maintainers = [p[0] for p in meta.Session.query(distinct(Package.maintainer)) if p[0]]

        maintset = set(maintainers)
        c.maintainers = maintset

        return search_params

