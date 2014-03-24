import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import Package, User
import ckan.model.meta as meta
import itertools as itertools


def get_package_creators():

    packages = meta.Session.query(Package).all()
    users = meta.Session.query(User).all()

    matched_users = []
    users_set = ([])

    for p in packages:
        user = itertools.ifilter(lambda x: x.id == p.creator_user_id, users)

        if(user):
            matched_users.append(user)

    if(matched_users):
        users_set = ([matched_users])

    print(users_set)

    return users_set


class ExtendSearchPlugin(plugins.SingletonPlugin):
    '''Extends the Ckan dataset/package search
    '''
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)

    get_package_creators()

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

