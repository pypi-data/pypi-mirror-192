'''
Mica search query.
'''

import json
import sys
import pycurl
import obiba_mica.core as core
import csv

def add_arguments(parser):
    '''
    Add tags command specific options
    '''
    parser.add_argument('--out', '-o', required=False, help='Output file (default is stdout).')
    parser.add_argument('--target', '-t', required=True, choices=['variable', 'dataset', 'study', 'population', 'dce', 'network'],
                        help='Document type to be searched for.')
    parser.add_argument('--query', '-q', required=False, help='Query that filters the documents. If not specified, no filter is applied.')
    parser.add_argument('--start', '-s', required=False, type=int, default=0, help='Start search at document position.')
    parser.add_argument('--limit', '-lm', required=False, type=int, default=100, help='Max number of documents.')
    parser.add_argument('--locale', '-lc', required=False, default='en', help='The language for labels.')

def send_search_request(client, ws, query, verbose=False):
    '''
    Create a new request
    '''
    response = None
    try:
        request = client.new_request()
        if verbose:
            request.verbose()
        response = request.post().resource(ws).content_type_form().form({'query': query}).send()
    except Exception as e:
        print(e, file=sys.stderr)
    except pycurl.error as error:
        errno, errstr = error
        print('An error occurred: ', errstr, file=sys.stderr)

    return response.as_json()

def as_rql(name, args):
    return name + '(' + ','.join(args) + ')'

def append_rql(query, target, select, sort, start, limit, locale):
    _fields = as_rql('fields(', select) + ')'
    _sort = as_rql('sort', sort)
    _limit = as_rql('limit', [str(start), str(limit)])
    statement = ','.join([_fields, _limit, _sort])
    # normalize
    q = query
    if q == None or q == '':
        q = target + '()'

    # hack: replace target call with statement
    if target + '()' in q:
        q = q.replace(target + '()', target + '(' + statement + ')')
    elif target + '(' in q:
        q = q.replace(target + '(', target + '(' + statement + ',')
    else:
        q = target + '(' + statement + '),' + q

    return q + ',locale(' + locale + ')'

def extract_label(labels, locale='en', locale_key='lang', value_key='value'):
    if not labels:
        return None
    label_und = None
    if labels:
        for label in labels:
            if label[locale_key] == locale:
                return label[value_key]
            if label[locale_key] == 'und':
                label_und = label[value_key]
    return label_und if label_und else ''

def new_writer(out, headers):
    file = sys.stdout
    if out:
        file = open(out, 'w')
    writer = csv.DictWriter(file, fieldnames=headers, escapechar='"', quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writeheader()
    return writer

def to_string(value):
    if value == None:
        return ''
    return str(value)

def flatten(content, locale='en'):
    flat = {}
    for key in list(content.keys()):
        value = content[key]
        if type(value) is dict:
            fvalue = flatten(value, locale)
            for k in fvalue:
                nk = key + '.' + k if k != locale else key
                flat[nk] = fvalue[k]
        elif type(value) is list:
            flat[key] = '|'.join(map(to_string, value))
        else:
            flat[key] = to_string(value)
    return flat

def search_networks(args, client):
    q = append_rql(args.query, 'network', ['*'], ['id'], args.start, args.limit, args.locale)
    ws = core.UriBuilder(['networks', '_rql']).build()
    res = send_search_request(client, ws, q, args.verbose)
    if 'networkResultDto' in res and 'obiba.mica.NetworkResultDto.result' in res['networkResultDto']:
        headers = ['id','name','acronym','description','studyIds']
        for item in res['networkResultDto']['obiba.mica.NetworkResultDto.result']['networks']:
            if 'content' in item:
                item['flat'] = flatten(json.loads(item['content']), args.locale)
                for key in list(item['flat'].keys()):
                    if key not in headers:
                        headers.append(key)
        writer = new_writer(args.out, headers)
        for item in res['networkResultDto']['obiba.mica.NetworkResultDto.result']['networks']:
            row = {
                'id': item['id'],
                'name': extract_label(item['name'], args.locale),
                'description': extract_label(item['description'], args.locale) if 'description' in item else '',
                'acronym': extract_label(item['acronym'], args.locale),
                'studyIds': '|'.join(item['studyIds']) if 'studyIds' in item else ''
            }
            if 'flat' in item:
                for key in item['flat']:
                    row[key] = item['flat'][key]
            writer.writerow(row)

def search_studies(args, client):
    q = append_rql(args.query, 'study', ['acronym', 'name', 'objectives', 'model'], ['id'], args.start, args.limit, args.locale)
    ws = core.UriBuilder(['studies', '_rql']).build()
    res = send_search_request(client, ws, q, args.verbose)
    if 'studyResultDto' in res and 'obiba.mica.StudyResultDto.result' in res['studyResultDto']:
        headers = ['id','name','acronym','objectives']
        for item in res['studyResultDto']['obiba.mica.StudyResultDto.result']['summaries']:
            if 'content' in item:
                item['flat'] = flatten(json.loads(item['content']), args.locale)
                for key in list(item['flat'].keys()):
                    if key not in headers:
                        headers.append(key)
        writer = new_writer(args.out, headers)
        for item in res['studyResultDto']['obiba.mica.StudyResultDto.result']['summaries']:
            row = {
                'id': item['id'],
                'name': extract_label(item['name'], args.locale),
                'objectives': extract_label(item['objectives'], args.locale) if 'objectives' in item else '',
                'acronym': extract_label(item['acronym'], args.locale)
            }
            if 'flat' in item:
                for key in item['flat']:
                    row[key] = item['flat'][key]
            writer.writerow(row)

def search_study_populations(args, client):
    q = append_rql(args.query, 'study', ['populations.name','populations.description','populations.model'], ['id'], args.start, args.limit, args.locale)
    ws = core.UriBuilder(['studies', '_rql']).build()
    res = send_search_request(client, ws, q, args.verbose)
    if 'studyResultDto' in res and 'obiba.mica.StudyResultDto.result' in res['studyResultDto']:
        headers = ['id','name','description','studyId']
        for item in res['studyResultDto']['obiba.mica.StudyResultDto.result']['summaries']:
            if 'populationSummaries' in item:
                for pop in item['populationSummaries']:
                    if 'content' in pop:
                        pop['flat'] = flatten(json.loads(pop['content']), args.locale)
                        for key in list(pop['flat'].keys()):
                            if key not in headers:
                                headers.append(key)
        writer = new_writer(args.out, headers)
        for item in res['studyResultDto']['obiba.mica.StudyResultDto.result']['summaries']:
            if 'populationSummaries' in item:
                for pop in item['populationSummaries']:
                    row = {
                        'id': item['id'] + ':' + pop['id'],
                        'name': extract_label(pop['name'], args.locale),
                        'description': extract_label(pop['description'], args.locale) if 'description' in pop else '',
                        'studyId': item['id']
                    }
                    if 'flat' in pop:
                        for key in pop['flat']:
                            row[key] = pop['flat'][key]
                    writer.writerow(row)

def search_study_dces(args, client):
    q = append_rql(args.query, 'study', ['populations.dataCollectionEvents'], ['id'], args.start, args.limit, args.locale)
    ws = core.UriBuilder(['studies', '_rql']).build()
    res = send_search_request(client, ws, q, args.verbose)
    if 'studyResultDto' in res and 'obiba.mica.StudyResultDto.result' in res['studyResultDto']:
        headers = ['id','name','description','studyId', 'populationId', 'start', 'end']
        for item in res['studyResultDto']['obiba.mica.StudyResultDto.result']['summaries']:
            if 'populationSummaries' in item:
                for pop in item['populationSummaries']:
                    if 'dataCollectionEventSummaries' in pop:
                        for dce in pop['dataCollectionEventSummaries']:
                            if 'content' in dce:
                                dce['flat'] = flatten(json.loads(dce['content']), args.locale)
                                for key in list(dce['flat'].keys()):
                                    if key not in headers:
                                        headers.append(key)
        writer = new_writer(args.out, headers)
        for item in res['studyResultDto']['obiba.mica.StudyResultDto.result']['summaries']:
            if 'populationSummaries' in item:
                for pop in item['populationSummaries']:
                    if 'dataCollectionEventSummaries' in pop:
                        for dce in pop['dataCollectionEventSummaries']:
                            row = {
                                'id': item['id'] + ':' + pop['id'] + dce['id'],
                                'name': extract_label(dce['name'], args.locale),
                                'description': extract_label(dce['description'], args.locale) if 'description' in dce else '',
                                'studyId': item['id'],
                                'populationId': item['id'] + ':' + pop['id'],
                                'start': dce['start'] if 'start' in dce else '',
                                'end': dce['end'] if 'end' in dce else ''
                            }
                            if 'flat' in dce:
                                for key in dce['flat']:
                                    row[key] = dce['flat'][key]
                            writer.writerow(row)


def search_datasets(args, client):
    q = append_rql(args.query, 'dataset', ['*'], ['id'], args.start, args.limit, args.locale)
    ws = core.UriBuilder(['datasets', '_rql']).build()
    res = send_search_request(client, ws, q, args.verbose)
    if 'datasetResultDto' in res and 'obiba.mica.DatasetResultDto.result' in res['datasetResultDto']:
        headers = ['id','name','acronym','description', 'variableType', 'entityType', 'studyId', 'populationId', 'dceId']
        for item in res['datasetResultDto']['obiba.mica.DatasetResultDto.result']['datasets']:
            if 'content' in item:
                item['flat'] = flatten(json.loads(item['content']), args.locale)
                for key in list(item['flat'].keys()):
                    if key not in headers:
                        headers.append(key)
        writer = new_writer(args.out, headers)
        for item in res['datasetResultDto']['obiba.mica.DatasetResultDto.result']['datasets']:
            study_id = ''
            population_id = ''
            dce_id = ''
            if 'obiba.mica.CollectedDatasetDto.type' in item:
                study_id = item['obiba.mica.CollectedDatasetDto.type']['studyTable']['studyId']
                population_id = study_id + ':' + item['obiba.mica.CollectedDatasetDto.type']['studyTable']['populationId']
                dce_id = item['obiba.mica.CollectedDatasetDto.type']['studyTable']['dceId']
            if 'obiba.mica.HarmonizedDatasetDto.type' in item:
                study_id = item['obiba.mica.HarmonizedDatasetDto.type']['harmonizationTable']['studyId']
                population_id = study_id + ':' + item['obiba.mica.HarmonizedDatasetDto.type']['harmonizationTable']['populationId']
            row = {
                'id': item['id'],
                'name': extract_label(item['name'], args.locale),
                'acronym': extract_label(item['acronym'], args.locale),
                'description': extract_label(item['description'], args.locale) if 'description' in item else '',
                'variableType': item['variableType'],
                'entityType': item['entityType'],
                'studyId': study_id,
                'populationId': population_id,
                'dceId': dce_id
            }
            if 'flat' in item:
                for key in item['flat']:
                    row[key] = item['flat'][key]
            writer.writerow(row)

def search_variables(args, client):
    q = append_rql(args.query, 'variable', ['*'], ['id'], args.start, args.limit, args.locale)
    ws = core.UriBuilder(['variables', '_rql']).build()
    res = send_search_request(client, ws, q, args.verbose)

    def category_label(category):
        if 'attributes' in category:
            labels = [extract_label(label['values'], args.locale) for label in [a for a in category['attributes'] if a['name'] == 'label']]
            return labels[0] if len(labels)>0 else ''
        else:
            return ''

    if 'variableResultDto' in res and 'obiba.mica.DatasetVariableResultDto.result' in res['variableResultDto']:
        headers = ['id','name','label','description','valueType','nature','categories','categories.missing','categories.label',
                   'datasetId','studyId','populationId','dceId',
                   'variableType','mimeType','unit','referencedEntityType','repeatable','occurrenceGroup']
        for item in res['variableResultDto']['obiba.mica.DatasetVariableResultDto.result']['summaries']:
            if 'annotations' in item:
                for annot in item['annotations']:
                    key = annot['taxonomy'] + '.' + annot['vocabulary']
                    if key not in headers:
                        headers.append(key)
        writer = new_writer(args.out, headers)
        for item in res['variableResultDto']['obiba.mica.DatasetVariableResultDto.result']['summaries']:
            row = {
                'id': item['id'],
                'name': item['name'],
                'label': extract_label(item['variableLabel'], args.locale) if 'variableLabel' in item else '',
                'description': extract_label(item['description'], args.locale) if 'description' in item else '',
                'datasetId': item['datasetId'],
                'studyId': item['studyId'],
                'populationId': item['populationId'] if 'populationId' in item else '',
                'dceId': item['dceId'] if 'dceId' in item else '',
                'variableType': item['variableType'],
                'valueType': item['valueType'] if 'valueType' in item else '',
                'nature': item['nature'] if 'nature' in item else '',
                'mimeType': item['mimeType'] if 'mimeType' in item else '',
                'unit': item['unit'] if 'unit' in item else '',
                'referencedEntityType': item['referencedEntityType'] if 'referencedEntityType' in item else '',
                'repeatable': item['repeatable'] if 'repeatable' in item else '',
                'occurrenceGroup': item['occurrenceGroup'] if 'occurrenceGroup' in item else ''
            }
            if 'categories' in item:
                row['categories'] = '|'.join([c['name'] for c in item['categories']])
                row['categories.missing'] = '|'.join([str(c['missing']) for c in item['categories']])
                row['categories.label'] = '|'.join(map(category_label, item['categories']))
            if 'annotations' in item:
                for annot in item['annotations']:
                    key = annot['taxonomy'] + '.' + annot['vocabulary']
                    row[key] = annot['value']
            writer.writerow(row)

def do_command(args):
    '''
    Execute search command
    '''
    client = core.MicaClient.build(core.MicaClient.LoginInfo.parse(args))
    if args.target == 'network':
        search_networks(args, client)
    elif args.target == 'study':
        search_studies(args, client)
    elif args.target == 'population':
        search_study_populations(args, client)
    elif args.target == 'dce':
        search_study_dces(args, client)
    elif args.target == 'dataset':
        search_datasets(args, client)
    elif args.target == 'variable':
        search_variables(args, client)
