import ckan
import pylons
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.model import User, Package, Group
import ckan.model.meta as meta
from ckan.lib.base import c
from sqlalchemy import distinct
from helpers import extend_search_convert_local_to_utc_timestamp

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

        start_date = extend_search_convert_local_to_utc_timestamp(extras.get('ext_startdate'))
        end_date = extend_search_convert_local_to_utc_timestamp(extras.get('ext_enddate'))
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

        context = {'model': ckan.model,
                   'session': ckan.model.Session,
                   'user': pylons.c.user}

        #set permission level: read (default is edit)
        data_dict = {'user': pylons.c.user, 'permission': 'read'}
        #get list of organisations that the user is a member of
        orgs = ckan.logic.get_action('organization_list_for_user')(context, data_dict)

        #user doesn't belong to an organisation
        if not orgs:
            print ('User is not a member of any organisations!')
            c.maintainers = []
            return search_params

        #get a distinct list of members who belong to the organisations
        members = []
        for org in orgs:
            params = {'id': org['id'], 'object_type': 'user'}
            member_list = ckan.logic.get_action('member_list')(context, params)
            for m in member_list:
                members.append(m)

        memberset = set(members)


        #need the user name to match with the maintainer field
        current_user_name = None
        member_names = []
        for member in memberset:
            user = User.get(member[0])    #user id
            member_names.append(user.name)


        #get all maintainers
        maintainers = [p[0] for p in meta.Session.query(distinct(Package.maintainer)) if p[0]]
        maintset = set(maintainers)


        #filter maintainers by user-related organisation members
        results = maintset.intersection(member_names)
        c.maintainers = results


        return search_params

