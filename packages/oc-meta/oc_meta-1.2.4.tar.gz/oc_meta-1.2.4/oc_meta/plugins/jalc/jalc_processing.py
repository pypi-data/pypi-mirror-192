#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2022 Arcangelo Massari <arcangelo.massari@unibo.it>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.


from __future__ import annotations

from oc_idmanager import DOIManager, ISSNManager, ORCIDManager

from oc_meta.lib.csvmanager import CSVManager
from oc_meta.plugins.ra_processor import RaProcessor


class JalcProcessing(RaProcessor):
    def __init__(self, orcid_index:str=None, doi_csv:str=None):
        self.doi_set = CSVManager.load_csv_column_as_set(doi_csv, 'id') if doi_csv else None
        orcid_index = orcid_index if orcid_index else None
        self.orcid_index = CSVManager(orcid_index)
        self._issnm = ISSNManager()
        self._om = ORCIDManager()

    def csv_creator(self, item:dict) -> dict:
        doi_manager = DOIManager(data=dict(), use_api_service=False)
        data = item['data']
        doi = doi_manager.normalise(data['doi'], include_prefix=True)
        publisher = self.get_ja(data['publisher_list'])[0]['publisher_name'] if 'publisher_list' in data else ''
        title = self.get_ja(data['title_list'])[0]['title'] if 'title_list' in data else ''
        issue = data['issue'] if 'issue' in data else ''
        volume = data['volume'] if 'volume' in data else ''
        first_page = data['first_page'] if 'first_page' in data else ''
        first_page = f'"{first_page}"' if '-' in first_page else first_page
        last_page = data['last_page'] if 'last_page' in data else ''
        last_page = f'"{last_page}"' if '-' in last_page else last_page
        pages = ''
        if first_page:
            pages += first_page
            if last_page:
                pages += f'-{last_page}'
        metadata = {
            'id': doi,
            'title': title,
            'author': '; '.join(self.get_authors(data)),
            'issue': issue,
            'volume': volume,
            'venue': self.get_venue(data),
            'pub_date': self.get_pub_date(data),
            'pages': pages,
            'type': self.get_type(data),
            'publisher': publisher,
            'editor': ''
        }
        return self.normalise_unicode(metadata)
        
    @classmethod
    def get_ja(cls, field:list) -> list:
        if all('lang' in item for item in field):
            ja = [item for item in field if item['lang'] == 'ja']
            ja = list(filter(lambda x: x['type'] != 'before' if 'type' in x else x, ja))
            if ja:
                return ja
            en = [item for item in field if item['lang'] == 'en']
            en = list(filter(lambda x: x['type'] != 'before' if 'type' in x else x, en))
            if en:
                return en
        return field
        
    def get_authors(self, data:dict) -> list:
        authors = list()
        if 'creator_list' in data:
            for creator in data['creator_list']:
                sequence = creator['sequence'] if 'sequence' in creator else ''
                names = creator['names'] if 'names' in creator else ''
                ja_name = self.get_ja(names)[0]
                last_name = ja_name['last_name'] if 'last_name' in ja_name else ''
                first_name = ja_name['first_name'] if 'first_name' in ja_name else ''
                full_name = ''
                if last_name:
                    full_name += last_name
                    if first_name:
                        full_name += f', {first_name}'
                if full_name:
                    authors.append((sequence, full_name))
                if 'researcher_id_list' in creator:
                    print(data)
        return [author[1] for author in sorted(authors, key=lambda x: x[0])]
    
    def get_venue(self, data:dict) -> str:
        venue_name = ''
        if 'journal_title_name_list' in data:
            candidate_venues = self.get_ja(data['journal_title_name_list'])
            if candidate_venues:
                full_venue = [item for item in candidate_venues if 'type' in item if item['type'] == 'full']
                if full_venue:
                    venue_name = full_venue[0]['journal_title_name']
                elif candidate_venues:
                    venue_name = candidate_venues[0]['journal_title_name']
        if 'journal_id_list' in data:
            journal_ids = {journal_id['journal_id'] for journal_id in data['journal_id_list'] 
                if journal_id['type'] == 'ISSN'}
        else:
            journal_ids = list()
        venue_ids = list()
        for journal_id in journal_ids:
            self.issn_worker(journal_id, venue_ids)
        return f"{venue_name} [{' '.join(venue_ids)}]" if venue_ids else venue_name

    @classmethod
    def get_type(cls, data:dict) -> str:
        content_type = data['content_type']
        if content_type == 'JA':
            br_type = 'journal article'
        elif content_type == 'BK':
            br_type = 'book'
        elif content_type == 'RD':
            br_type = 'dataset'
        elif content_type == 'EL':
            br_type = 'other'
        elif content_type == 'GD':
            br_type = 'other'
        return br_type
    
    @classmethod
    def get_pub_date(cls, data) -> str:
        pub_date_dict = data['publication_date'] if 'publication_date' in data else ''
        pub_date_list = list()
        year = pub_date_dict['publication_year'] if 'publication_year' in pub_date_dict else ''
        if year:
            pub_date_list.append(year)
            month = pub_date_dict['publication_month'] if 'publication_month' in pub_date_dict else ''
            if month:
                pub_date_list.append(month)
                day = pub_date_dict['publication_day'] if 'publication_day' in pub_date_dict else ''
                if day:
                    pub_date_list.append(day)
        return '-'.join(pub_date_list)