import {Injectable} from '@angular/core';
import {Observable, of} from 'rxjs';
import {SResult} from './sresult/SResult';
import {environment} from '../environments/environment';
import {HttpClient, HttpHeaders} from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class DataService {

  constructor(private http: HttpClient) {
  }

  MOCK_SRESULTS = {
    hits: {
      hits: [{_source: {title: 'title', annotation: 'text one', genre: '', year: 2018, author: 'Nikita'}, _score: 54},
        {_source: {title: 'Cats', annotation: 'Cats are nice', score: 44, genre: '', year: 2018, author: 'Nikita'}},
        {
          _source: {
            title: 'Dogs',
            annotation: 'I don\'t like dogs',
            score: 38,
            genre: '',
            year: 2018,
            author: 'Nikita'
          }
        },
        {_source: {title: 'Rain', annotation: 'Cats and dogs', score: 20, genre: '', year: 2018, author: 'Nikita'}}
      ]
    }
  };


  TITLE_SEARCH_DATA = {
    query: {
      simple_query_string: {
        query: '',
        fields: [
          'title^2'
        ]
      }
    }
  }

  httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': environment.base_url
    }),
    method: 'GET'
  };

// @ts-ignore
  getData(query: string, author_query: string, author_check: boolean, annotation_check: boolean): Observable<> {
    if (environment.mock_api) {
      return of(this.MOCK_SRESULTS);
    }
    return this.queryData(query, author_query, author_check, annotation_check);
  }

// @ts-ignore
  queryData(query: string, author_query: string, author_check: boolean, annotation_check: boolean): Observable<> {
    const url = environment.base_url + environment.search_request_template;
    const req_data = this.TITLE_SEARCH_DATA;
    req_data.query.simple_query_string.query = query;
    if (author_check) {
      req_data.query['match'] = {};
      req_data.query['match']['author'] = author_query;
    }
    if (annotation_check) {
      req_data.query.simple_query_string.fields.push('annotation');
    }
    console.log(req_data);
    return this.http.post<SResult[]>(url, req_data, this.httpOptions);
  }
}
