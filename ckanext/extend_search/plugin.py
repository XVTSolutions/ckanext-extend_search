import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def get_stuff():
    'A function to get stuff'

    groups = toolkit.get_action('group_list')(
        data_dict={'sort': 'packages desc', 'all_fields': True})

    groups = groups[:10]

    return groups


class ExtendSearchPlugin(plugins.SingletonPlugin):
    '''Extends the Ckan dataset/package search

    '''
    # Declare that this plugin will implement ITemplateHelpers.
    plugins.implements(plugins.ITemplateHelpers)

    # Declare that this class implements IConfigurer.
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):

        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        # 'templates' is the path to the templates dir, relative to this
        # plugin.py file.
        toolkit.add_template_directory(config, 'templates')

    def get_helpers(self):
        '''Register the get_stuff() function above as a template
        helper function.

        '''
        # Template helper function names should begin with the name of the
        # extension they belong to, to avoid clashing with functions from
        # other extensions.
        return {'extend_search_get_stuff': get_stuff}