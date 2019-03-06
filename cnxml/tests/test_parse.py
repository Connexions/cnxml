import pytest
from lxml import etree

from cnxml.parse import NSMAP, parse_metadata


@pytest.fixture
def xml(datadir):
    with (datadir / 'valid_collection.xml').open() as fb:
        xml = etree.parse(fb)
    return xml


def test_parse(xml):
    # Call the target
    props = parse_metadata(xml)

    expected_props = {
        'abstract': (
            'This introductory, algebra-based, two-semester college physics '
            'book is grounded with real-world examples, illustrations, and '
            'explanations to help students grasp key, fundamental physics '
            'concepts. This online, fully editable and customizable title '
            'includes learning objectives, concept questions, links to labs '
            'and simulations, and ample practice opportunities to solve '
            'traditional physics application problems.'
        ),
        'authors': ('OpenStaxCollege',),
        'created': '2012/01/23 13:03:30.293 US/Central',
        'id': 'col11406',
        'keywords': (
            'ac circuits',
            'atomic physics',
            'bioelectricity',
            'biological and medical applications',
            'circuits',
        ),
        'language': 'en',
        'license_url': 'http://creativecommons.org/licenses/by/4.0/',
        'licensors': ('OSCRiceUniversity',),
        'maintainers': ('OpenStaxCollege', 'cnxcap'),
        'print_style': 'ccap-physics',
        'revised': '2015/07/27 12:55:32.442 GMT-5',
        'subjects': ('Mathematics and Statistics', 'Science and Technology'),
        'title': 'College Physics',
        'version': '1.9',
    }
    # Verify the metadata
    assert props == expected_props


# https://github.com/Connexions/cnx-press/issues/17
def test_parse_without_abstract(xml):
    # Remove the abstract
    elm = xml.xpath('//md:abstract',
                    namespaces=NSMAP)[0]
    elm.getparent().remove(elm)

    # Call the target
    props = parse_metadata(xml)

    # Verify the abstract is empty
    assert props['abstract'] is None


def test_parse_with_cnxml_abstract(xml):
    abstract = '<list><item>A</item><item>C</item><item>E</item></list>'

    # Find and modify the abstract to include wrapping text
    elm = xml.xpath('//md:abstract', namespaces=NSMAP)[0]
    elm.text = "FOO "
    abstract_elms = etree.fromstring(abstract)
    abstract_elms.tail = " BAR"
    elm.append(abstract_elms)

    elm.tail = " BAR"

    # Call the target
    props = parse_metadata(xml)

    expected_abstract = 'FOO {} BAR'.format(abstract)
    # parse the metadata into a dict and check for the abstract.
    assert props['abstract'] == expected_abstract